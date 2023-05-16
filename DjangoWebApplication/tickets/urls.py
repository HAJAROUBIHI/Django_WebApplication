from django.urls import path
from . import views

urlpatterns = [
    path('tickets/', views.tickets, name='tickets'),
    path('tickets/<int:ticket_id>/book/', views.book_ticket, name='book_ticket'),
    path('tickets/<int:ticket_id>/cancel/', views.cancel_ticket, name='cancel_ticket'),
]
