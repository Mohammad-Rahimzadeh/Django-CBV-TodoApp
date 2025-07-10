from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import View
from django.utils import timezone
from datetime import datetime

from .models import Profile
from .forms import SignupForm, EditProfileForm
from todo.models import Item



# Create your views here.

class LoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('todo:list-item') 

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    



class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('todo:list-item')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)




class ProfileView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(user=self.request.user).first()
        context['get_current_date'] = datetime.now().strftime("%Y/ %m/ %d")
        context['get_current_time'] = timezone.now().time().strftime('%H:%M')
        context['all_tasks'] = Item.objects.filter(author=self.request.user)
        return context
    


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile.first()
    



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('account:login')