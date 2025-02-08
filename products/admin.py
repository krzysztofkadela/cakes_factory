from django.contrib import admin
from .models import Category, Flavor, Size, Product, Review

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")

@admin.register(Flavor)
class FlavorAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "flavor", "price", "available")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "rating", "created_at")
