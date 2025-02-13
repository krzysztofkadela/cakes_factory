from django.urls import path
from .views import cart_add, cart_view, cart_remove, checkout, order_history, custom_order, cart_update

urlpatterns = [
    path("cart/add/<int:product_id>/", cart_add, name="cart_add"),
    path("cart/", cart_view, name="cart_view"),
    path("cart/update/<int:product_id>/<int:size_id>/", cart_update, name="cart_update"),
    path("cart/remove/<int:product_id>/<int:size_id>/", cart_remove, name="cart_remove"),
    path("checkout/", checkout, name="checkout"),
    path("orders/", order_history, name="order_history"),
    path("custom_order/<int:product_id>/", custom_order, name="custom_order"),
]