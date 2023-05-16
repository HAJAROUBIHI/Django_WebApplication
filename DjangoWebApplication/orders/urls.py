from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/pay/', views.pay_order, name='pay_order'),
]
