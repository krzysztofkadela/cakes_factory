# users/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CustomUserForm
from .models import CustomUser
from orders.models import Order  # Order model is imported

# User profile

@login_required
def user_profile(request):
    """User profile page displaying personal details and order history."""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "users/profile.html", {
        "user": request.user,
        "orders": orders,
    })

# User profile update

@login_required
def edit_profile(request):
    """Allow a logged-in user to edit shipping/billing details."""
    if request.method == "POST":
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("user_profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})