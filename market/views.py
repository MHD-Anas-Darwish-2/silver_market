from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from datetime import datetime
import json
from market.forms import CategoryForm, ProductForm
from market.utils import count_cart_items, get_cart
from .models import *

# Create your views here.

def store(request):
    # filter
    query = request.GET.get("q") if request.GET.get("q") else ''
    start_price = request.GET.get("start_price") if request.GET.get("start_price") else 0
    end_price = request.GET.get("end_price") if request.GET.get("end_price") else 10000000

    if query or start_price or end_price != 10000000: # if user search
        products = Product.objects.filter((Q(name__icontains=query) | Q(description__icontains=query)) & Q(price__gte=start_price) & Q(price__lte=end_price))
    
    else:
        products = Product.objects.all().order_by('number_of_sales')[:10] # top 10 sales

    context = {
        'products': products,
        'count_cart_items': count_cart_items(request),
    }
    return render(request, 'market/store.html', context)

def product(request, slug): # view product
    product_item = Product.objects.get(slug=slug)

    context = {
        'product': product_item,
        'count_cart_items': count_cart_items(request),
    }
    return render(request, 'market/product.html', context)

def cart(request):
    if request.user.is_authenticated:
        cart = get_cart(request)
    else:
        return redirect('account_login')

    
    context = {
        'count_cart_items': cart['count_cart_items'],
        'items': cart['items'],
        'total': cart['total'],
    }
    return render(request, 'market/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        cart = get_cart(request)
    else:
        return redirect('account_login')

    
    context = {
        'count_cart_items': cart['count_cart_items'],
        'items': cart['items'],
        'total': cart['total'],
    }
    return render(request, 'market/checkout.html', context)

def updateCart(request): # add and remove items from cart
    data = json.loads(request.body)
    product_id = data["productId"]
    action = data["action"]
    user = request.user

    product = Product.objects.get(id=product_id)
    order, create = Order.objects.get_or_create(user=user, complete=False)
    order_item, create = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1

    elif action == 'remove':
        order_item.quantity -= 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse("Item was added", safe=False)

@user_passes_test(lambda u: u.is_superuser)
def create_product(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()     

    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    count_cart_items = order.get_cart_items
    
    context = {
        'count_cart_items': count_cart_items,
        'form': form,
    }
    return render(request, 'market/create_or_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def update_product(request, slug):
    product = Product.objects.get(slug=slug)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect('store')

    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    count_cart_items = order.get_cart_items
    
    context = {
        'count_cart_items': count_cart_items,
        'form': form,
    }
    return render(request, 'market/create_or_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, slug):
    product = Product.objects.get(slug=slug)
    product.delete()
    return JsonResponse("Product was removed", safe=False)

def categories(request):
    categories = Category.objects.all()

    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    count_cart_items = order.get_cart_items
    
    context = {
        'count_cart_items': count_cart_items,
        'categories': categories,
    }
    return render(request, 'market/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def create_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()          

    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    count_cart_items = order.get_cart_items
    
    context = {
        'count_cart_items': count_cart_items,
        'form': form,
    }
    return render(request, 'market/create_or_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return JsonResponse("Category was removed", safe=False)

@user_passes_test(lambda u: u.is_superuser)
def orders(request):
    orders = Order.objects.all()

    context = {
        'orders': orders,
    }
    return render(request, 'market/orders.html', context)

@user_passes_test(lambda u: u.is_superuser)
def order(request, id):
    order = Order.objects.get(id=id)
    order_items = OrderItem.objects.filter(order=order)
    
    shipping_address = False
    if order.complete:
        shipping_address = ShippingAddress.objects.get(order=order)

    context = {
        'order': order,
        'order_items': order_items,
        'shipping_address': shipping_address,
    }
    return render(request, 'market/order.html', context)

def process_order(request):
    if request.user.is_authenticated:
        transaction_id = datetime.now().timestamp()
        data = json.loads(request.body)

        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
            
        total = float(data['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True

            order_items = OrderItem.objects.filter(order=order)
            for order_item in order_items:
                order_item.product.number_of_sales += order_item.quantity
                order_item.save()
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

        return JsonResponse('Payment complete!', safe=False)
    else:
        return redirect('account_login')