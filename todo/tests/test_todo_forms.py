from django.test import TestCase
from datetime import datetime, timedelta

from ..forms import ItemCreateForm, ItemUpdateForm


class TestForms(TestCase):
    def test_item_create_form_with_valid_data(self):
        due_time = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
        form = ItemCreateForm(
            data={
                "title": "test",
                "due_date": datetime.now().date(),
                "due_time": due_time,
                "priority": "High priority",
            }
        )
        self.assertTrue(form.is_valid())

    def test_item_create_form_with_invalid_data(self):
        due_time = (datetime.now() + timedelta(minutes=-1)).strftime("%H:%M")
        form = ItemCreateForm(
            data={
                "title": "test",
                "due_date": datetime.now().date(),
                "due_time": due_time,
                "priority": "High priority",
            }
        )
        self.assertFalse(form.is_valid())

    def test_item_update_form_with_valid_data(self):
        due_time = (datetime.now() + timedelta(minutes=20)).strftime("%H:%M")
        tomorrow = datetime.now().date() + timedelta(days=1)
        form = ItemUpdateForm(
            data={
                "title": "test",
                "note": "test",
                "priority": "High priority",
                "due_date": tomorrow,
                "due_time": due_time,
                "important": True,
            }
        )
        self.assertTrue(form.is_valid())

    def test_item_update_form_with_invalid_data(self):
        due_time = (datetime.now() + timedelta(minutes=20)).strftime("%H:%M")
        yesterday = datetime.now().date() + timedelta(days=-1)
        form = ItemUpdateForm(
            data={
                "title": "test",
                "note": "test",
                "priority": "High priority",
                "due_date": yesterday,
                "due_time": due_time,
                "important": True,
            }
        )
        self.assertFalse(form.is_valid())
