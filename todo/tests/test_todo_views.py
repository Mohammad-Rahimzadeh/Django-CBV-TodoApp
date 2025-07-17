from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, timedelta
from django.db.models.signals import post_save

from account.models import User, Profile
from account.models import save_profile
from ..models import Item



class TestTodoViews(TestCase):
    post_save.disconnect(save_profile, sender=User)
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@test.com',
            password='13475479mr'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='test_first_name',
            last_name='test_last_name',
            task_count=1,
            completed_task_count=1,
        )
        
        self.item = Item.objects.create(
            author=self.profile,
            title="test",
            complete=False,
            important=True,
            note="test",
            priority="Low priority",
            due_date=datetime.now().date(),
            due_time=(datetime.now() + timedelta(minutes=-1)).strftime("%H:%M"),
            show_item=True,
        )

    def test_todo_list_item_url_successful_response(self):
        self.client.force_login(self.user)
        url = reverse('todo:list-item')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='todo/item_list.html')

    def test_todo_single_item_logged_in_response(self):
        self.client.force_login(self.user)
        url = reverse('todo:single-item', kwargs={'pk':self.item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)