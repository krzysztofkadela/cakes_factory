from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import NewsletterForm
from .models import NewsletterSubscriber

#newslatter function

def newsletter_signup(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            
            # Check if email is already subscribed
            if NewsletterSubscriber.objects.filter(email=email).exists():
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"error": "⚠️ This email is already subscribed!"}, status=400)
                messages.warning(request, "⚠️ This email is already subscribed!")
            else:
                form.save()
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"success": "✅ Thank you for subscribing!"}, status=200)
                messages.success(request, "✅ Thank you for subscribing!")

            return redirect("home")  # Redirect after form submission

        # If form is invalid
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": form.errors}, status=400)

        messages.error(request, "⚠️ Invalid email address. Please try again.")
        return redirect("home")

    return redirect("home")  # Redirect if accessed without POST
