# from django.test import TestCase
# from django.urls import reverse, resolve

# from ..views import ListItemView, SingleItemView


# class TestUrls(TestCase):
#     def test_todo_item_list_urls_resolve(self):
#         url = reverse("todo:list-item")
#         self.assertEqual(resolve(url).func.view_class, ListItemView)

#     def test_todo_item_single_urls_resolve(self):
#         url = reverse("todo:single-item", kwargs={'pk':1})
#         self.assertEqual(resolve(url).func.view_class, SingleItemView)
