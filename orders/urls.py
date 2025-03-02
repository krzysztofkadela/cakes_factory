from django.urls import path
from . import views, webhook  # ✅ Importing views and webhooks correctly

urlpatterns = [
    # Cart Management
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/update/<int:product_id>/<int:size_id>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:product_id>/<int:size_id>/", views.cart_remove, name="cart_remove"),

    # Checkout & Orders
    path("checkout/", views.checkout_page, name="checkout"),
    path("orders/", views.order_history, name="order_history"),
    path("custom_order/<int:product_id>/", views.custom_order, name="custom_order"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    path("update-order-status/<int:order_id>/", views.update_order_status, name="update_order_status"),

    # Stripe Checkout & Webhooks
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),
    path("success/", views.payment_success, name="payment_success"),
    path("cancel/", views.payment_cancel, name="payment_cancel"),

    # ✅ Secure Stripe Webhook
    path("webhook/", webhook.webhook, name="stripe_webhook"),
]