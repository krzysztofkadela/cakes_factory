from django.urls import path
from . import views, webhook  # Importing views and webhook

urlpatterns = [
    # Cart Management
    path("cart/add/<int:product_id>/",
         views.cart_add,
         name="cart_add"),
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/update/<int:product_id>/<int:size_id>/",
         views.cart_update, name="cart_update"),
    path("cart/remove/<int:product_id>/<int:size_id>/",
         views.cart_remove, name="cart_remove"),

    # Checkout & Orders
    path("checkout/", views.checkout_page, name="checkout"),
    path("orders/", views.order_history, name="order_history"),
    path("order/<str:order_number>/",
         views.order_detail, name="order_detail"),
    path("order/<str:order_number>/retry/",
         views.retry_payment, name="retry_payment"),
    path("update-order-status/<int:order_id>/",
         views.update_order_status, name="update_order_status"),

    # Stripe Checkout & Webhooks
    path("create-checkout-session/",
         views.create_checkout_session,
         name="create_checkout_session"),
    path("success/", views.payment_success, name="payment_success"),
    path("cancel/", views.payment_cancel, name="payment_cancel"),

    # Secure Stripe Webhook
    path("webhook/", webhook.webhook, name="stripe_webhook"),

    # ✅ Admin Order Management
    path("admin/manage-orders/", views.manage_orders, name="manage_orders"),
    path("admin/update-order-status/<str:order_number>/<str:status>/",
         views.update_order_status, name="update_order_status"),
]