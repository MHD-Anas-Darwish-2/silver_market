from django.urls import path
from .views import *

urlpatterns = [
    path('', store, name="store"),
    path('items/<slug:slug>/', product, name="product"),

    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('update_cart/', updateCart, name="update_cart"),
    path('process_order/', process_order, name="process_order"),

    path('product/create/', create_product, name="create_product"),
    path('product/update/<slug:slug>/', update_product, name="update_product"),
    path('product/delete/<slug:slug>/', delete_product, name="delete_product"),

    path('categories/', categories, name="categories"),
    path('category/create/', create_category, name="create_category"),
    path('category/delete/<int:id>/', delete_category, name="delete_category"),

    path('orders/', orders, name="orders"),
    path('orders/<int:id>/', order, name="order"),
]
