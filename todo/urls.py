from django.urls import path
from . import views


app_name = "todo"

urlpatterns = [
    path("", views.ListItemView.as_view(), name="list-item"),
    path("item/<int:pk>", views.SingleItemView.as_view(), name="single-item"),
    path("create/", views.CreateItemView.as_view(), name="create-item"),
    path("update/<int:pk>/", views.UpdateItemView.as_view(), name="update-item"),
    path("delete/<int:pk>/", views.DeleteItemView.as_view(), name="delete-item"),
    path("complete/<int:pk>/", views.CompleteItemView.as_view(), name="complete-item"),
    path(
        "important/add/<int:pk>/",
        views.AddToImportantItemView.as_view(),
        name="add-important-item",
    ),
    path(
        "important/remove/<int:pk>/",
        views.RemoveImportantItem.as_view(),
        name="remove-important-item",
    ),
    path("important-item", views.ImportantItemView.as_view(), name="important-item"),
    path("expired-item", views.ExpiredItemView.as_view(), name="expired-item"),
    path("items/", views.SearchItemView.as_view(), name="search-item"),
]
