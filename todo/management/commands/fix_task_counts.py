from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from todo.models import Item

User = get_user_model()


class Command(BaseCommand):
    help = "Fix task counts for all users"

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            profile = user.profile.first()
            if profile:
                items = Item.objects.filter(author=user)
                profile.task_count = items.count()
                profile.completed_task_count = items.filter(complete=True).count()
                profile.save()
