import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from decimal import Decimal
from orders.models import Order

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    order_id = request.session.get('order_id')
    
    # Handle case where order_id is None or invalid
    if not order_id:
        return redirect('home')  # Redirect to home or another appropriate page
    
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        amount = Decimal(total_cost).quantize(Decimal('0.01'))  # Ensure proper decimal formatting

        result = gateway.transaction.sale({
            'amount': str(amount),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')  # Redirect to payment success page
        
        else:
            return redirect('payment:canceled')  # Redirect to payment cancellation page
    
    else:
        client_token = gateway.client_token.generate()
        return render(request, "payment/process.html", {
            'order': order,
            'client_token': client_token
        })


def payment_done(request):
    return render(request, "payment/payment_done.html")

def payment_canceled(request):
    return render(request, "payment/payment_canceled.html")