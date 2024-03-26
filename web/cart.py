from decimal import Decimal
from django.conf import settings

CART_SESSION_KEY = getattr(settings, 'CART_SESSION_KEY', 'cart')


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1, price=None):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.sale_price),
            }
        self.cart[product_id]['quantity'] += quantity
        self.save()
        
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrease_quantity(self, product):
        product_id = str(product.id)
        if product_id in self.cart and self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1
            self.save()
        elif product_id in self.cart and self.cart[product_id]['quantity'] == 1:
            self.remove(product)  # Remove the product if quantity becomes zero.

    def save(self):
        self.session.modified = True

    def get_cart(self):
        return self.cart.items() 
    
    def get_total_price(self, item):
        return Decimal(item['quantity']) * Decimal(item['price'])

    def cart_total(self):
        return sum(
            Decimal(item[1]['quantity']) * Decimal(item[1]['price'])
            for item in self.get_cart()
        )

    def get_product_quantity(self, product):
        product_id = str(product.id)
        item = self.cart.get(product_id)
        if item:
            return item['quantity']
        return 0
    
    def clear(self):
        del self.session[CART_SESSION_KEY]
        self.save()
