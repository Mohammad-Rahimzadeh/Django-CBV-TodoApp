from django.contrib import admin
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "priority",
        "due_date",
        "due_time",
        "complete",
        "important",
        "author",
    ]


# Register your models here.

admin.site.register(Item, ItemAdmin)
