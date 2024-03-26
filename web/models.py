from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.contrib.auth.models import User
import uuid
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Slider(models.Model):
    title = models.CharField(max_length=150)
    background_image = models.ImageField(upload_to="slider")
    description=models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    


class Category(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="category",blank=True,null=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="SubCategory")
    description=models.TextField(blank=True,null=True)
    our_top_pics = models.BooleanField(default=False)
    is_home = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def get_products(self):
        return Product.objects.filter(subcategory=self)
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    image = models.ImageField(upload_to="product")
    description = HTMLField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_arrival = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    is_home = models.BooleanField(default=False)

    def get_images(self):
        return ProductImage.objects.filter(product=self)
    
    def __str__(self):
        return self.name
    


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product")


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_product_name(self):
        return self.product

    def get_total_price(self):
        res = float(self.quantity) * float(self.product.sale_price)
        return round(res,2)

    def cart_total(self):
        return float(sum(item.get_total_price() for item in Cart.objects.filter(user=self.user)))

    def __str__(self):
        return f"{self.product} - {self.quantity}"
    

def generate_order_id():
    timestamp = timezone.now().strftime("%y%m%d")
    unique_id = uuid.uuid4().hex[:6]
    return f"{timestamp}{unique_id.upper()}"


class Order(models.Model):
    PAYMENT = (("COD", "Cash On Delivery"), ("OP", "Online Payment") )
    unique_transaction_id = models.UUIDField(
        unique=True, editable=False, blank=True, null=True
    )
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True) 
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payable = models.DecimalField(max_digits=10, decimal_places=2, default=0.00 ,blank=True, null=True)
    order_id = models.CharField(max_length=255, default=generate_order_id)
    is_ordered = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT,
        default="COD",
    )
    
    

    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address_line_1 = models.CharField("Complete Address", max_length=100)
    address_line_2 = models.CharField("Landmark", max_length=100)
    state = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100)
    pin_code = models.IntegerField()
    mobile_no = models.CharField(max_length=15)
    alternative_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_status = models.CharField(
        max_length=50,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Placed", "Order Placed"),
            ("Shipped", "Order Shipped"),
            ("InTransit", "In Transit"),
            ("Delivered", "Order Delivered"),
            ("Cancelled", "Order Cancelled"),
        ),
    )
    payment_status = models.CharField(
        max_length=50,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Failed", "Failed"),
            ("Success", "Success"),
            ("Cancelled", "Cancelled"),
        ),
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ("-id",)

    def get_items(self):
        return OrderItem.objects.filter(order=self)

    def get_grand_total(self):
        total = self.payable + self.service_fee + self.shipping_fee
        return total

    def order_total(self):
        return float(sum([item.subtotal() for item in self.get_items()]))
    

    def get_user_absolute_url(self):
        return reverse("web:order_detail", kwargs={"order_id": self.order_id})
    
    def get_absolute_url(self):
        return reverse("web:dash_order_detail", kwargs={"pk": self.pk})
    
    
    @staticmethod
    def get_list_url():
        return reverse_lazy("web:order_list")
    
    # def get_update_url(self):
    #     return reverse_lazy("web:order_update", kwargs={"pk": self.pk})
    
    # def get_delete_url(self):
    #     return reverse_lazy("web:order_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.order_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey("web.Product", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.order} - {self.product}"

    def subtotal(self):
        return self.price * self.quantity
    

