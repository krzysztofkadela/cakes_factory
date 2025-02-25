# users/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import Order  # Order model is imported

@login_required
def user_profile(request):
    """User profile page displaying personal details and order history."""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "users/profile.html", {
        "user": request.user,
        "orders": orders,
    })