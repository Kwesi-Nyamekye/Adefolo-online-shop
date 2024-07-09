from django.urls import path
from . import views

app_name = "payment"
urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('payment_done/', views.payment_done, name='done'),
    path('payment_canceled/', views.payment_canceled, name='canceled'), 
]
