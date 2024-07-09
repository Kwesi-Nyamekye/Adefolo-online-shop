# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def send_order_confirmation_email(order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order nr. {order.id}'
        message = f'Dear {order.first_name},\n\n' \
                  f'You have successfully placed an order.' \
                  f'Your order ID is {order.id}.'
        mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
        return mail_sent
    except Order.DoesNotExist:
        # Handle the case where the order does not exist
        return False
    except Exception as e:
        # Log the exception
        print(f'Error sending email: {e}')
        return False
