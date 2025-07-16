from django.test import TestCase
from datetime import datetime, timedelta

from ..models import Item
from account.models import User, Profile



class TestTodoModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com", password="13475479mr")
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="test_first_name",
            last_name="test_last_name",
            task_count=1,
            completed_task_count=1,
        )

    def test_item_model_with_valid_data(self):
        due_time = (datetime.now() + timedelta(minutes=-1)).strftime("%H:%M")
        item = Item.objects.create(
            author=self.profile,
            title="test",
            complete=False,
            important=True,
            note="test",
            priority="Low priority",
            due_date=datetime.now().date(),
            due_time=due_time,
            show_item=True,
        )
        self.assertTrue(Item.objects.filter(pk=item.id).exists())
