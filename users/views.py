from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .forms import CustomUserForm
from .models import CustomUser
from orders.models import Order
from products.models import Product  # Ensure you have a Product model in products app

@login_required
def user_profile(request):
    """
    User profile page displaying personal details and order history.
    If user is superuser, also display all users, all orders, and all products.
    """
    # Regular user order history
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    # Prepare context for regular user
    context = {
        "user": request.user,
        "orders": orders,
    }

    # If user is superuser, pass admin data
    if request.user.is_superuser:
        all_users = CustomUser.objects.all()
        all_orders = Order.objects.all().order_by("-created_at")
        all_products = Product.objects.all()

        context.update({
            "all_users": all_users,
            "all_orders": all_orders,
            "all_products": all_products,
        })

    return render(request, "users/profile.html", context)

@login_required
def edit_profile(request):
    """
    Allow a logged-in user to edit shipping/billing details.
    """
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

@login_required
@user_passes_test(lambda u: u.is_superuser)
def toggle_user_status(request, user_id):
    """Activate or deactivate a user's account."""
    target_user = get_object_or_404(CustomUser, id=user_id)
    if target_user.is_active:
        target_user.is_active = False
        messages.info(request, f"User {target_user.username} deactivated.")
    else:
        target_user.is_active = True
        messages.success(request, f"User {target_user.username} activated.")
    target_user.save()
    return redirect("user_profile")