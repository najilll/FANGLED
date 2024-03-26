from django.contrib import admin
from django.urls import path
from . import views

app_name = "web"

urlpatterns = [
    path("",views.IndexView.as_view(), name="index"),
    path("product_detail/<str:slug>/", views.Product_DetailView.as_view(), name="product_detail"),
    # path("signin/", views.SigninView.as_view(), name="signin"),
    # path("signup/", views.SignupView.as_view(), name="signup"),
    path('subcategory/<str:slug>/', views.SubCategoryDetailView.as_view(), name='subcategory_detail'),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    #cart
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.CartAddView.as_view(), name='add_cart'),
    path('cart-item-clear/<str:item_id>/', views.ClearCartItemView.as_view(), name='clear_cart_item'),
    path('cart/minus/', views.MinusToCartView.as_view(), name='minus_to_cart'),
    path('cart-clear/', views.ClearCartView.as_view(), name='clear_cart'),
    #payment
    path("payment/<str:pk>/", views.PaymentView.as_view(), name="payment"),
    path("callback/<str:pk>/", views.callback, name="callback"),
]