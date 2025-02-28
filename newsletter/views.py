from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import NewsletterForm
from .models import NewsletterSubscriber

#newslatter function

def newsletter_signup(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Prevent duplicate subscriptions
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.warning(request, "You are already subscribed!")
            else:
                form.save()
                messages.success(request, "Thank you for subscribing!")
            return redirect("home")  # Redirect to home after subscribing
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return redirect("home")