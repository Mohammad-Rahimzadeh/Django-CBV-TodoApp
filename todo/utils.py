from datetime import date

from .models import Item


def hide_past_items():
    today = date.today()
    past_items = Item.objects.filter(due_date__lt=today, show_item=True)
    past_items.update(show_item=False)
