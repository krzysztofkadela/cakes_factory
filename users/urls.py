from django.urls import path
from .views import user_profile, edit_profile, toggle_user_status
from . import views

urlpatterns = [
    path("profile/", user_profile, name="user_profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("toggle_user_status/<int:user_id>/", toggle_user_status, name="toggle_user_status"),
    path("manage/products/", views.manage_products, name="manage_products"),
    path("manage/subscriptions/", views.manage_subscriptions, name="manage_subscriptions"),
    path("manage/subscriptions/toggle/<int:subscriber_id>/", views.toggle_subscription, name="toggle_subscription"),
    path("manage/subscriptions/delete/<int:subscriber_id>/", views.delete_subscription, name="delete_subscription"),
    path("manage/users/", views.manage_users, name="manage_users"),
    path("manage/orders/", views.manage_orders, name="manage_orders"),
]