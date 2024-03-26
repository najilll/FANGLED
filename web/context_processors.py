from .models import Category,Cart

def main_context(request):
    category=Category.objects.all()[:3]
    user = None
    cart_count = 0
    cart_items = []
    if request.user.is_authenticated:
        user = request.user
        cart_count = Cart.objects.filter(user=user).count()
        cart_items = Cart.objects.filter(user=user)
    context={
        "header_category":category,
        "cart_items": cart_items,  # Use the initialized cart_items variable
        "cart_count": cart_count,
    }
    return context
