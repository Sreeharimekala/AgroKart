from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.catalog.models import Product
from .models import Cart, CartItem
from .models import Order, OrderItem
from apps.accounts.models import Address
from django.contrib import messages

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    total = sum(item.total_price() for item in items)

    return render(request, 'orders/cart.html', {
        'cart': cart,
        'items': items,
        'total': total
    })


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    quantity = int(request.POST.get('quantity', 1))
    item.quantity = quantity
    item.save()

    return redirect('view_cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()

    return redirect('view_cart')





@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    if not items:
        return redirect('view_cart')

    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        address_id = request.POST.get('address')
        address = Address.objects.get(id=address_id, user=request.user)

        total = sum(item.total_price() for item in items)

        # Create Order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amount=total
        )

        # Create Order Items
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            # Reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        # Clear cart
        items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('my_orders')

    return render(request, 'orders/checkout.html', {
        'items': items,
        'addresses': addresses
    })



@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'orders/my_orders.html', {
        'orders': orders
    })
