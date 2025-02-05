from django.urls import path
from .views import ProductListView, ProductDetailView, filter_products

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('filter/', filter_products, name='filter_products'),  # Search & Filter URL
]