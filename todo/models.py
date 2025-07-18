from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.utils import timezone

from account.models import Profile



# Other functions


def default_deadline_time():
    return (timezone.now() + timedelta(minutes=1)).time()


# Create your models here.


class Item(models.Model):
    class Meta:
        verbose_name = "Items"
        verbose_name_plural = "Items"

    PRIORITY_STATUS_CHOICES = (
        ("High priority", "High priority"),
        ("Medium priority", "Medium priority"),
        ("Low priority", "Low priority"),
    )

    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile"
    )
    title = models.CharField(max_length=255)
    complete = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True, default="")
    priority = models.CharField(
        max_length=15, choices=PRIORITY_STATUS_CHOICES, blank=True, null=True
    )
    due_date = models.DateField(default=date.today)
    due_time = models.TimeField(default=default_deadline_time)
    show_item = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.title)

    def clean(self):
        now = timezone.now()
        now_time = now.time()
        today = date.today()

        if self.due_date == today and self.due_time < now_time:
            raise ValidationError("due time cannot be in the past for today.")

        if self.due_date < today:
            raise ValidationError("due date cannot be in the past.")

    @property
    def is_expired(self):
        now = timezone.now()
        if self.due_date < now.date():
            return True
        if self.due_date == now.date() and self.due_time < now.time():
            return True
        return False
