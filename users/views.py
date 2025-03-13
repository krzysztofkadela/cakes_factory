from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import CustomUserForm
from .models import CustomUser
from orders.models import Order
from products.models import Product
from newsletter.models import NewsletterSubscriber

@login_required
def user_profile(request):
    """User profile displaying personal details and order history."""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    context = {
        "user": request.user,
        "orders": orders,
    }

    return render(request, "users/profile.html", context)

@login_required
def edit_profile(request):
    """Allow user to edit their details."""
    if request.method == "POST":
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("user_profile")
        else:
            messages.error(request, "Please correct errors below.")
    else:
        form = CustomUserForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def toggle_user_status(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)
    target_user.is_active = not target_user.is_active
    target_user.save()
    status = "activated" if target_user.is_active else "deactivated"
    messages.success(request, f"User {target_user.username} {status}.")
    return redirect("manage_users")

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_users(request):
    users = CustomUser.objects.all()
    return render(request, "users/manage_users.html", {"users": users})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_orders(request):
    orders = Order.objects.all().order_by("-created_at")
    return render(request, "users/manage_orders.html", {"orders": orders})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_products(request):
    products = Product.objects.all()
    return render(request, "users/manage_products.html", {"products": products})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_subscriptions(request):
    subscriptions = NewsletterSubscriber.objects.all()
    return render(request, "users/manage_subscriptions.html", {"subscriptions": subscriptions})