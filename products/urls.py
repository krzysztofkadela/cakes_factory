from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    filter_products,
    add_product,
    edit_product
)
from . import views


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('filter/', filter_products, name='filter_products'),
    path("add/", add_product, name="add_product"),
    path("edit/<int:product_id>/", edit_product, name="edit_product"),
    path(
        "delete/<int:product_id>/",
        views.delete_product,
        name="delete_product"
    ),
]
