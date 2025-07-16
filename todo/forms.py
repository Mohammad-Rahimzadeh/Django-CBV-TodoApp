from django import forms
from datetime import date

from .models import Item


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "due_date", "due_time", "priority"]


class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "note", "priority", "due_date", "due_time", "important"]
        widgets = {
            "due_date": forms.DateInput(
                attrs={"type": "date", "min": date.today().isoformat()}
            ),
            "due_time": forms.TimeInput(attrs={"type": "time"}),
        }
