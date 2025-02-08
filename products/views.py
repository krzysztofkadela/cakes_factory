from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Review

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Override to optionally filter by category slug passed as ?category=slug."""
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        if category_slug:
            # Filter by category__slug, not category__id
            queryset = queryset.filter(category__slug=category_slug)
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'


def filter_products(request):
    """
    Advanced filtering: search by name (q), price range, category slug, allergen-free.
    Renders the same product_list.html but with a filtered queryset.
    """
    query = request.GET.get('q')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category_slug = request.GET.get('category')
    allergen_free = request.GET.get('allergen_free')

    products = Product.objects.all()

    # Text search
    if query:
        products = products.filter(name__icontains=query)

    # Price range
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    # Category filter by slug
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Exclude allergen info if allergen_free is checked
    if allergen_free:
        products = products.exclude(allergen_info__icontains="nuts")

    return render(request, 'products/product_list.html', {'products': products})