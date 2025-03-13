from django.urls import path
from .views import home_view, test_messages

urlpatterns = [
    path("", home_view, name="home"),
]