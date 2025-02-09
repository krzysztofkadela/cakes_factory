from .models import OrderItem

def cart_context(request):
    cart = request.session.get('cart', {})

    total_items = sum(item['quantity'] for item in cart.values()) if cart else 0
    total_price = sum(float(item['price']) * int(item['quantity']) for item in cart.values()) if cart else 0.00

    return {
        'cart_items': total_items,
        'cart_total_price': total_price
    }