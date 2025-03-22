from .models import Category


def categories_context(request):
    """Make categories available in templates"""
    return {
        'categories': Category.objects.all()
    }