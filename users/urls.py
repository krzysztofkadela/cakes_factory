from django.urls import path
from .views import user_profile, edit_profile

urlpatterns = [
    path("profile/", user_profile, name="user_profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
]