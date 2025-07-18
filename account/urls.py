from django.urls import path
from . import views


app_name = "account"


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("edit-profile/", views.EditProfileView.as_view(), name="edit-profile"),
]
