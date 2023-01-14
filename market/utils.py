from .models import Order
from django.shortcuts import redirect

def count_cart_items(request):
    if (request.user.is_authenticated):
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        count_cart_items = order.get_cart_items
    else:
        count_cart_items = 0
    return count_cart_items

def get_cart(request):

    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    count_cart_items = order.get_cart_items
    items = order.orderitem_set.all()
    total = order.get_cart_total

    context = {
        'count_cart_items': count_cart_items,
        'items': items,
        'total': total,
    }
    return context