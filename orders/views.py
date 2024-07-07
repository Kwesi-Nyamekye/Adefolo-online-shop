from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from .forms import OrderCreatedForm
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    
    if request.method == "POST":
        form = OrderCreatedForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return redirect('orders:order_created', order_id=order.id)
    else:
        form = OrderCreatedForm()
    
    return render(request, "orders/order_create.html", {'cart': cart, 'form': form})

def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_created.html', {'order': order})
