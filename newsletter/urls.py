from django.urls import path
from .views import newsletter_signup
from . import views

urlpatterns = [
    path("newsletter-signup/", newsletter_signup, name="newsletter_signup"),
]