from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import Http404
from django.db.models import Q
import calendar
from django.utils import timezone
from datetime import timedelta, time

from .models import Item
from .forms import ItemCreateForm, ItemUpdateForm
from account.models import Profile
from .utils import hide_past_items


# Create your views here.


class FilteredItemView(LoginRequiredMixin, ListView):
    model = Item
    context_object_name = "items"
    template_name = "item_list.html"
    redirect_field_name = settings.LOGIN_URL
    important_only = False

    def get_queryset(self):
        hide_past_items()

        profile = Profile.objects.filter(user=self.request.user).first()
        base_queryset = self.model.objects.filter(author=profile)

        now = timezone.now()
        today = now.date()
        now_time = now.time()

        today_items = base_queryset.filter(due_date=today)
        expired_items = today_items.filter(due_time__lt=now_time)
        active_items = today_items.filter(due_time__gte=now_time, show_item=True)

        if self.important_only:
            active_items = active_items.filter(important=True)

        date_filter = self.request.GET.get("day")
        if date_filter:
            date_filter = date_filter.lower()
            for i in range(7):
                target_date = today + timedelta(days=i)
                weekday_name = calendar.day_name[target_date.weekday()].lower()
                if weekday_name == date_filter:
                    active_items = base_queryset.filter(
                        due_date=target_date,
                        due_time__gte=now_time if target_date == today else time(0, 0),
                        show_item=True,
                    )
                    expired_items = base_queryset.filter(
                        due_date=target_date,
                        due_time__lt=now_time if target_date == today else time(0, 0),
                    )
                    break
            else:
                active_items = self.model.objects.none()
                expired_items = self.model.objects.none()

        self.expired_items = expired_items
        self.active_items = active_items
        return active_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        upcoming_days = []

        for i in range(3):
            target_date = today + timedelta(days=i)
            weekday_eng = calendar.day_name[target_date.weekday()].lower()
            weekday_short = target_date.strftime("%a").lower()
            upcoming_days.append(
                {
                    "name": weekday_eng,
                    "label": weekday_short,
                }
            )
        context["form"] = ItemCreateForm()
        context["profile"] = Profile.objects.filter(user=self.request.user).first()
        context["get_current_date"] = timezone.now().strftime("%Y/ %m/ %d")
        context["get_current_time"] = timezone.now().time().strftime("%H:%M")
        context["today"] = timezone.now().date()
        context["tomorrow"] = timezone.now().date() + timedelta(days=1)
        context["day_after"] = timezone.now().date() + timedelta(days=2)
        context["upcoming_days"] = upcoming_days
        context["active_items"] = self.active_items
        context["expired_items"] = self.expired_items
        return context


class ListItemView(FilteredItemView):
    important_only = False


class ImportantItemView(FilteredItemView):
    important_only = True


class SingleItemView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = "todo/single_item.html"
    redirect_field_name = settings.LOGIN_URL
    context_object_name = "item"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        profile = Profile.objects.filter(user=self.request.user).first()
        if obj.author != profile:
            raise Http404("Not allowed.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context["form"] = ItemCreateForm()
        context["profile"] = profile
        context["get_current_date"] = timezone.now().strftime("%Y/ %m/ %d")
        context["get_current_time"] = timezone.now().time().strftime("%H:%M")
        return context


class CreateItemView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemCreateForm
    success_url = reverse_lazy("todo:list-item")
    template_name = "todo/item_list.html"

    def get_context_data(self, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context["items"] = Item.objects.filter(author=profile, show_item=True)
        context["profile"] = profile
        context["get_current_date"] = timezone.localdate()
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.author = profile
        response = super().form_valid(form)
        profile = Profile.objects.filter(user=self.request.user).first()
        if profile:
            profile.task_count += 1
            profile.save()

        return response

    def form_invalid(self, form):
        return redirect("todo:list-item")


class UpdateItemView(UpdateView):
    model = Item
    form_class = ItemUpdateForm
    template_name = "todo/partials/item_edit_form.html"

    def post(self, request, pk):
        profile = Profile.objects.get(user=self.request.user)
        item = get_object_or_404(Item, pk=pk, author=profile)
        item.title = request.POST.get("title", item.title)
        item.note = request.POST.get("note", item.note)
        item.priority = request.POST.get("priority", item.priority)
        item.due_time = request.POST.get("due_time", item.due_time)
        item.due_date = request.POST.get("due_date", item.due_date)
        item.important = "important" in request.POST
        item.save()
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("todo:list-item")


class DeleteItemView(View):
    def post(self, request, pk):
        profile = Profile.objects.get(user=self.request.user)
        item = get_object_or_404(Item, pk=pk, author=profile)
        if profile:
            profile.task_count = max(0, profile.task_count - 1)
            if item.complete:
                profile.completed_task_count = max(0, profile.completed_task_count - 1)
            profile.save()

        item.delete()
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("todo:list-item")


class CompleteItemView(View):
    def post(self, request, pk):
        profile = Profile.objects.get(user=self.request.user)
        item = get_object_or_404(Item, pk=pk, author=profile)
        item.complete = True
        item.save()

        profile = Profile.objects.filter(user=self.request.user).first()
        if profile:
            profile.completed_task_count += 1
            profile.save()
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url:
                return redirect(next_url)

        return redirect("todo:list-item")


class AddToImportantItemView(View):
    def post(self, request, pk):
        profile = Profile.objects.get(user=self.request.user)
        item = get_object_or_404(Item, pk=pk, author=profile)
        item.important = True
        item.save()
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("todo:list-item")


class RemoveImportantItem(View):
    def post(self, request, pk):
        profile = Profile.objects.get(user=self.request.user)
        item = get_object_or_404(Item, pk=pk, author=profile)
        item.important = False
        item.save()
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("todo:list-item")


class SearchItemView(FilteredItemView):
    def get_queryset(self):
        query = self.request.GET.get("q")
        profile = Profile.objects.get(user=self.request.user)
        queryset = self.model.objects.filter(author=profile)
        if query:
            queryset = queryset.filter(title__icontains=query)
        self.active_items = queryset
        self.expired_items = self.model.objects.none()
        return queryset


class ExpiredItemView(LoginRequiredMixin, ListView):
    model = Item
    template_name = "todo/expired_items.html"
    context_object_name = "expired_items"

    def get_queryset(self):
        now = timezone.now()
        today = now.date()
        now_time = now.time()
        profile = Profile.objects.get(user=self.request.user)
        
        return (
            Item.objects.filter(
                author=profile,
            )
            .filter(
                (Q(due_date__lt=today)) | (Q(due_date=today) & Q(due_time__lt=now_time))
            )
            .order_by("-due_date", "-due_time")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.filter(user=self.request.user).first()
        context["get_current_date"] = timezone.now().strftime("%Y/ %m/ %d")
        context["get_current_time"] = timezone.now().time().strftime("%H:%M")
        return context
