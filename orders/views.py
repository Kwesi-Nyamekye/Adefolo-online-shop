# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from .forms import OrderCreatedForm
from cart.cart import Cart
from django.urls import reverse
from .tasks import send_order_confirmation_email

def order_create(request):
    cart = Cart(request)
    
    if request.method == "POST":
        form = OrderCreatedForm(request.POST)
        if form.is_valid():
            # Save the order from the form data
            order = form.save()
            
            # Create OrderItem instances for each item in the cart
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Clear the cart after creating order items
            cart.clear()
            
            # Delay execution of the Celery task to send order confirmation email
            send_order_confirmation_email.delay(order.id)
            
            # Store the order ID in session for further processing
            request.session['order_id'] = order.id
            
            # Redirect to the payment processing page
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreatedForm()
    
    # Render the order creation form
    return render(request, "orders/order_create.html", {'cart': cart, 'form': form})

def order_created(request, order_id):
    # Retrieve the order details based on order_id
    order = get_object_or_404(Order, id=order_id)
    
    # Render the order created confirmation page
    return render(request, 'orders/order_created.html', {'order': order})
