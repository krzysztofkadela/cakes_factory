from django.urls import path
from .views import home_view, test_messages

urlpatterns = [
    path("", home_view, name="home"),
    path("test_messages/", test_messages, name="test_messages"),  # 👈 Add this line
]