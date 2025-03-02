from django.urls import path
from .views import user_profile, edit_profile, toggle_user_status

urlpatterns = [
    path("profile/", user_profile, name="user_profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("toggle_user_status/<int:user_id>/", toggle_user_status, name="toggle_user_status"),
]