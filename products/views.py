from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Review

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

def filter_products(request):
    query = request.GET.get('q')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category = request.GET.get('category')
    allergen_free = request.GET.get('allergen_free')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    if category:
        products = products.filter(category=category)
    if allergen_free:
        products = products.exclude(allergen_info__icontains="nuts")

    return render(request, 'products/product_list.html', {'products': products})

