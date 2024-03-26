import razorpay
from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from . models import SubCategory,Product,OrderItem,Order,Slider
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect
from .cart import Cart 
from django.views.generic import ListView
from decimal import Decimal
from django.urls import reverse
from .forms import OrderForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY, settings.RAZOR_PAY_SECRET))

# Create your views here.
class IndexView(TemplateView):
    template_name = "web/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider'] = Slider.objects.filter(is_active=True)
        context["sub_categories"] = SubCategory.objects.filter(our_top_pics=True)
        context["arrival_product"] = Product.objects.filter(new_arrival=True)
        context["best_seller_product"] = Product.objects.filter(best_seller=True)
        context["sub_category_name"] = SubCategory.objects.filter(is_home=True)[:1]
        if context["sub_category_name"]:
            context["products"] = Product.objects.filter(subcategory=context["sub_category_name"]).filter(is_home=True)[:4]
        else:
            context["products"] = []  # Set empty list if no subcategory is marked as is_home
        
        return context
    

# class DetailView(TemplateView):
#     template_name = "web/product.html"

# class Product_DetailView(TemplateView):
#     template_name = "web/detail.html"

class SigninView(TemplateView):
    template_name = "web/signin.html"

class SignupView(TemplateView):
    template_name = "web/signup.html"


class SubCategoryDetailView(DetailView):
    model = SubCategory
    template_name = "web/product.html"


class Product_DetailView(DetailView):
    model = Product
    template_name = "web/detail.html"

# class CartView(TemplateView):
#     template_name = "web/cart.html"
    

class CheckoutView(View):
    template_name = "web/checkout.html"
    
    def get(self, request):
        cart = Cart(request)
        
    
        print("hello")
        cart_items = []
        
        for item_id, item_data in cart.get_cart():
            product = get_object_or_404(Product,id=item_id)
            quantity = item_data["quantity"]
            # total_price = Decimal(item_data["sale_price"]) * quantity
            cart_items.append({
                "product": product,
                "quantity": quantity,
                # "total_price": total_price,
            })

           
            
                
            
            
        print(cart_items)
        context = {
            'cart_items': cart_items,
            'cart_total': cart.cart_total(),
        }
        return render(request, self.template_name, context)
        
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        user = request.user
        
        if form.is_valid():
            order = form.save(commit=False)
            
            if user.is_authenticated:
                order.user = user
            else:
                order.user = None
                
            payment_method = request.POST.get('paymentMethod')
            
            total = request.POST.get('total_price')
            order.payment_method = payment_method
            
            
            order.subtotal=total
            order.payable=total
            
            
                
            order.total = total
            order.save()
            
            for item_id, item_data in cart.get_cart():
                variant = get_object_or_404(Product, id=item_id)
                quantity = item_data["quantity"]
                

                price = Decimal(item_data["price"])
                    
                order_item = OrderItem.objects.create(
                    order=order,
                    product=variant,
                    price=price,
                    quantity=quantity,
                )
                order_item.save()
                
            
            if order.payment_method == "OP":
                return redirect("web:payment", pk=order.pk)
            else:
                cart.clear()
                return redirect("web:payment",pk=order.pk)
            
        else:
            print(form.errors)
            context = {
                "cart_items": cart_items,
                "cart_total": sum(item["total_price"] for item in cart_items),
                "form": form,
            }
            return render(request, self.template_name, context)
    
    
    def get_cart_items(self, cart):
        cart_items = []
        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(Product, id=item_id)
            quantity = item_data['quantity']
            total_price = Decimal(item_data['price']) * quantity
            if item_data.get('wholesale_price'):
                wholesale_total_price = Decimal(item_data['wholesale_price']) * quantity
            else:
                wholesale_total_price = Decimal(0)
                
            cart_items.append({
                'product': variant,
                'quantity': quantity,
                'total_price': total_price if not wholesale_total_price else wholesale_total_price,
            })
        return cart_items
    

class PaymentView(View):
    def get(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        currency = "INR"
        amount = float(order.payable) * 100
        razorpay_order = client.order.create(
            {"amount": amount, "currency": currency, "payment_capture": "1"}
        )
        razorpay_order_id = razorpay_order["id"]
        order.razorpay_order_id = razorpay_order_id
        order.save()
        

        context = {
            "object": order,
            "amount": amount,
            "razorpay_key": settings.RAZOR_PAY_KEY,
            "razorpay_order_id": razorpay_order_id,
            "callback_url": f"{settings.DOMAIN}/callback/{order.pk}/",
        }
        return render(request, "web/payment.html", context=context)
    

@csrf_exempt
def callback(request, pk):
    order = get_object_or_404(Order, pk=pk)
    print(request.GET)
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        response_data = {
            "razorpay_order_id": provider_order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature_id,
        }

        order = Order.objects.get(razorpay_order_id=provider_order_id)
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = signature_id
        client = razorpay.Client(
            auth=(settings.RAZOR_PAY_KEY, settings.RAZOR_PAY_SECRET)
        )
        result = client.utility.verify_payment_signature(response_data)

        if result is not None:
            print("Signature verification successful")
            order.is_ordered = True
            order.order_status = "Placed"
            order.payment_status = "Success"
            order.save()


            
            print("email sent successfully")
            cart = Cart(request)
            cart.clear()
            
        else:
            print("Signature verification failed, please check the secret key")
            order.payment_status = "Failed"
            order.save()
        return render(request, "web/callback.html", {"object": order})
    else:
        print("Razorpay payment failed")
        return redirect("web:payment", pk=order.pk)


class CartView(ListView):
    template_name = 'web/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart = Cart(self.request)
        cart_items = []

        for item_id, item_data in cart.get_cart():
            product = get_object_or_404(Product,id=item_id)
            quantity = item_data["quantity"]
            total_price = Decimal(item_data["sale_price"]) * quantity
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "total_price": total_price,
            })

        return cart_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        cart_total = sum(
            Decimal(item[1]["quantity"]) * Decimal(item[1]["sale_price"])
            for item in cart.get_cart()
        )
        context["cart_total"] = cart_total
        return context
    

    
#cart
    
class CartView(View):
    def get(self, request):
        cart = Cart(request)
        cart_items = []

        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(Product, id=item_id)
            quantity = item_data['quantity']
            
            total_price = Decimal(item_data['price']) * quantity

            
            cart_items.append({
                'product': variant,
                'quantity': quantity,
                'total_price': total_price,
            })
                
                
        context = {
            'cart_items': cart_items,
            'cart_total': cart.cart_total(),
        }
        return render(request, "web/cart.html", context)


class CartAddView(View):
    def get(self, request):
        cart = Cart(request)
        cart_instance = cart.cart
        quantity = request.GET.get('quantity', 1)
        product_id = request.GET.get("product_id", '')
        price = request.GET.get("sale_price", None)
        variant = get_object_or_404(Product, pk=product_id)
        cart.add(variant, quantity=int(quantity),price=price)
        
       
        return JsonResponse({
            'quantity': cart.get_product_quantity(variant),
            'total_price': cart.get_total_price(cart_instance[product_id]),  
            'cart_total': cart.cart_total(),
            'cart_count': len(cart_instance),
            
        })
    
    
class ClearCartItemView(View):
    def get(self, request, item_id):
        cart = Cart(request)
        
        variant = get_object_or_404(Product, id=item_id)
        cart.remove(variant)
        return redirect('web:cart')


class MinusToCartView(View):
    def get(self, request):
        cart = Cart(request)
        cart_instance = cart.cart
        item_id = request.GET.get("item_id")
        variant = get_object_or_404(Product, id=item_id)
        cart.decrease_quantity(variant)
        return JsonResponse({
            'quantity':cart.get_product_quantity(variant),
            'total_price': cart.get_total_price(cart_instance[item_id]),
            'cart_total': cart.cart_total(),
        })
    

class ClearCartView(View):
    def get(self, request):
        cart = Cart(request)
        cart.clear()
        return redirect(reverse('web:index'))