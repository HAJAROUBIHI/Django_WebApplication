from django.urls import path
from . import views  # Import your views
from django.contrib.auth import views as auth_views
from .views import AccountCreateView, AccountUpdateView, AccountDeleteView,AccountListView, AccountDetailView
#from events.views import EventListView
from .views import payment, payment_success, payment_cancel



urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # Changed from 'views.login' to 'views.login_view'
    path('logout/', views.logout_view, name='logout'),  # Changed from 'views.logout' to 'views.logout_view'
    path('profile/user/', views.user_profile, name='user_profile'),  # New path for user profile
    path('profile/organizer/', views.organizer_profile_view, name='organizer_profile'),  
    path('profile/organizer/AllEvents', views.AllEvents, name='organizer_events'),  
    path('profile/update/', views.profile_update, name='profile_update'),  
    path('profile/user/update/', views.profile_update_u, name='profile_update_u'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('account/new/', AccountCreateView.as_view(), name='account-create'),
    path('account/<int:pk>/update/', AccountUpdateView.as_view(), name='account-update'),
    path('account/<int:pk>/delete/', AccountDeleteView.as_view(), name='account-delete'),
    path('accounts/', AccountListView.as_view(), name='account-list'),
    path('account/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('principal/', views.principal_page, name='principal_page'),
    #path('events/', EventListView.as_view(), name='event_list'),
    #path('orders/', EventListView.as_view(), name='event_list'),
    path('orders/user', views.user_orders, name='user_orders'),
    path('dashboard/user/', views.dashboard_user, name='dashboard_user'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('contactUs/', views.contact_u, name='contact_u'),
    path('aboutUs/', views.about_u, name='about_u'),
    path('remove-ticket/<int:order_id>/', views.remove_ticket, name='remove_ticket'),
    path('payment/<int:event_id>/', payment, name='payment'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/cancel/', payment_cancel, name='payment_cancel'),


]

