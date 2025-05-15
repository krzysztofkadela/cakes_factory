from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UserEditForm, CustomUserForm
from .models import CustomUser
from orders.models import Order
from products.models import Product
from newsletter.models import NewsletterSubscriber

User = get_user_model()


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
    users = User.objects.all()
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
    return render(
        request, "users/manage_products.html", {"products": products}
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_subscriptions(request):
    """View all newsletter subscribers."""
    subscribers = NewsletterSubscriber.objects.all().order_by("-subscribed_at")
    return render(
        request,
        "users/manage_subscriptions.html",
        {"subscribers": subscribers},
    )


@user_passes_test(lambda u: u.is_superuser)
def toggle_subscription(request, subscriber_id):
    """Enable or disable a newsletter subscription."""
    subscriber = get_object_or_404(NewsletterSubscriber, id=subscriber_id)
    subscriber.active = not subscriber.active
    subscriber.save()
    messages.success(
        request, f"Subscription status updated for {subscriber.email}."
    )
    return redirect("manage_subscriptions")


@user_passes_test(lambda u: u.is_superuser)
def delete_subscription(request, subscriber_id):
    """Delete a newsletter subscription."""
    subscriber = get_object_or_404(NewsletterSubscriber, id=subscriber_id)
    subscriber.delete()
    messages.success(
        request, f"Subscriber {subscriber.email} deleted successfully."
    )
    return redirect("manage_subscriptions")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def view_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, "users/view_user.html", {"user": user})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User details updated successfully.")
            return redirect("manage_users")
    else:
        form = UserEditForm(instance=user)
    return render(
        request, "users/edit_user.html", {"form": form, "user": user}
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect("manage_users")
    return render(request, "users/confirm_delete_user.html", {"user": user})
