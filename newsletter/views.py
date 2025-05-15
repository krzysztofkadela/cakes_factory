from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import NewsletterForm
from .models import NewsletterSubscriber


def newsletter_signup(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            # Check if already subscribed
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email
            )
            if not created:
                # Already exists
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse(
                        {"error": "⚠️ This email is already subscribed!"},
                        status=400,
                    )
                else:
                    messages.warning(
                        request, "⚠️ This email is already subscribed!"
                    )
            else:
                # Successfully subscribed
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse(
                        {"success": "✅ Thank you for subscribing!"},
                        status=200,
                    )
                else:
                    messages.success(request, "✅ Thank you for subscribing!")

            return redirect("home")

        else:
            # Invalid form (duplicate email, invalid format, etc.)
            errors = form.errors.get(
                "email", ["⚠️ Invalid email address. Please try again."]
            )
            error_message = errors[0]  # Get the first error message

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": error_message}, status=400)
            else:
                messages.error(request, error_message)
                return redirect("home")

    # Non-POST request => Redirect home
    return redirect("home")
