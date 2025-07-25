from django.contrib.admin.views.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import Product, Category
from .forms import ProductForm


class ProductListViewold(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        """Override to optionally filter by category
        slug passed as ?category=slug.
        """
        queryset = super().get_queryset()
        category_slug = self.request.GET.get("category")
        if category_slug:
            # Filter by category__slug, not category__id
            queryset = queryset.filter(category__slug=category_slug)
        return queryset


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get filters from URL parameters
        query = self.request.GET.get("q", "").strip()
        price_min = self.request.GET.get("price_min")
        price_max = self.request.GET.get("price_max")
        category_slug = self.request.GET.get("category", "").strip()
        allergen_free = self.request.GET.get("allergen_free")

        # If search button is clicked but input is empty, show error message
        if "q" in self.request.GET and not query:
            messages.error(self.request, "Please enter a search term.")

        # Apply search filter
        if query:
            queryset = queryset.filter(name__icontains=query)

        # Apply price filters
        if price_min:
            try:
                queryset = queryset.filter(price__gte=float(price_min))
            except ValueError:
                pass  # Ignore invalid values

        if price_max:
            try:
                queryset = queryset.filter(price__lte=float(price_max))
            except ValueError:
                pass  # Ignore invalid values

        # Apply category filter
        if category_slug:
            category = Category.objects.filter(slug=category_slug).first()
            if category:
                queryset = queryset.filter(category=category)

        # Apply allergen-free filter
        if allergen_free:
            queryset = queryset.exclude(allergen_info__icontains="nuts")

        return queryset

    def get_context_data(self, **kwargs):
        """Include all categories
        in the context for the dropdown menu.
        """
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"


def filter_products(request):
    """
    Advanced filtering: search by name (q),
    price range, category slug, allergen-free.
    Renders the same product_list.html but with a filtered queryset.
    """
    query = request.GET.get("q")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")
    category_slug = request.GET.get("category")
    allergen_free = request.GET.get("allergen_free")

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

    return render(
        request, "products/product_list.html", {"products": products}
    )


# Admin manage product functionality views:


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser)
def add_product(request):
    """Allows superusers to add a new product."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            # Redirect to profile page
            return redirect("manage_products")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm()

    return render(request, "products/add_product.html", {"form": form})


@user_passes_test(is_superuser)
def edit_product(request, product_id):
    """Allows superusers to edit an existing product."""
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("manage_products")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "products/edit_product.html",
        {"form": form, "product": product},
    )


@user_passes_test(is_superuser)
def delete_product(request, product_id):
    """Allows superusers to delete a product."""
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("manage_products")

    return render(
        request, "products/delete_product.html", {"product": product}
    )
