# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Account  
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, AccountUpdateForm
from django.contrib import messages
from .forms import UserRegisterForm, AccountRegisterForm  
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from events.models import Event
from orders.models import Order
from django.utils import timezone
from tickets.models import Ticket


from django.contrib import messages

from django.core.cache import cache
from django.contrib import messages

def dashboard_user(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        return redirect('payment', event_id=event_id)
    
    events = Event.objects.filter(status='approved')
    new_event_approved = False
    last_count = request.session.get('approved_event_count', 0)
    current_count = events.count()

    if current_count > last_count:
        new_event_approved = True
        request.session['approved_event_count'] = current_count
        messages.success(request, 'New event approved!')
    
    search_query = request.GET.get('search')
    search_results = None

    if search_query:
        # Effectuer la recherche en fonction de la query de recherche
        search_results = events.filter(location__icontains=search_query)
    
    return render(request, 'accounts/dashboard_user.html', {
        'events': events,
        'search_query': search_query,
        'search_results': search_results,
        'new_event_approved': new_event_approved,
    })
  

def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    print(f"Orders: {orders}")  
    context = {           
            'orders': orders
        }
    return render(request, 'accounts/user_orders.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        account_form = AccountRegisterForm(request.POST, request.FILES)
        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save()
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserRegisterForm()
        account_form = AccountRegisterForm()
    return render(request, 'accounts/register.html', {'user_form': user_form, 'account_form': account_form})

from django.contrib.auth.decorators import user_passes_test


from django.contrib.auth.decorators import login_required


def admin(request):
    return render(request, 'accounts/admin.html')


def principal_page(request):
    return render(request, 'accounts/principal_page.html')


def user_check(user):
    return user.account.type_user == 'simple_user'

def organizer_check(user):
    return user.account.type_user == 'organizer'


@login_required(login_url='login')
def user_profile(request):
    account = Account.objects.get(user=request.user)
    return render(request, 'accounts/user_profile.html', {'account': account})

@login_required(login_url='login')
def organizer_profile(request):
    account = Account.objects.get(user=request.user)
    return render(request, 'accounts/organizer_profile.html', {'account': account})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user_check(user):
                return redirect('user_profile')
            elif organizer_check(user):
                return redirect('organizer_profile')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


from .models import Account  
from events.models import Event

def organizer_profile_view(request):
    if request.user.is_authenticated:
        print(f"Authenticated User: {request.user.username}")  # print username of authenticated user
        events = Event.objects.filter(organizer=request.user)
        print(f"Events: {events}")  # print queryset of events
        context = {
            'account': Account.objects.get(user=request.user),
            'events': events
        }
        return render(request, 'accounts/organizer_profile.html', context)
    else:
        print("User is not authenticated.")  # print a message if user is not authenticated
        return redirect('login')  # replace 'login' with the name of your login url



@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        account_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user.account)

        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request, 'Your account has been updated!')
            
            if organizer_check(request.user):
                return redirect('organizer_profile')
            else:
                return redirect('user_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        account_form = AccountUpdateForm(instance=request.user.account)

    context = {
        'user_form': user_form,
        'account_form': account_form
    }

    return render(request, 'accounts/profile_update.html', context)


@login_required
def profile_update_u(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        account_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user.account)

        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request, 'Your account has been updated!')
            
            if organizer_check(request.user):
                return redirect('organizer_profile')
            else:
                return redirect('user_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        account_form = AccountUpdateForm(instance=request.user.account)

    context = {
        'user_form': user_form,
        'account_form': account_form
    }

    return render(request, 'accounts/profile_update_u.html', context)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Account

class AccountCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Account
    fields = ['full_name', 'type_user', 'profile_pic', 'date_of_birth', 'phone_number', 'address', 'bio']

    def test_func(self):
        return self.request.user.is_superuser

class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Account
    fields = ['full_name', 'type_user', 'profile_pic', 'date_of_birth', 'phone_number', 'address', 'bio']

    def test_func(self):
        return self.request.user.is_superuser

class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Account
    success_url = '/'

    def test_func(self):
        return self.request.user.is_superuser

class AccountListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Account
    context_object_name = 'accounts'
    template_name = 'accounts/account_list.html'
    ordering = ['-date_joined']

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(full_name__icontains=query)
        return qs

class AccountDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Account

    def test_func(self):
        return self.request.user.is_superuser

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

from django.http import HttpResponse

from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Send email with form data
        send_mail(
            'Contact Form Submission',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            email,
            ['youremail@example.com'],
            fail_silently=False,
        )
        
        return render(request, 'accounts/contact_success.html')
    else:
        return render(request, 'accounts/contact.html')

def contact_u(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Send email with form data
        send_mail(
            'Contact Form Submission',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            email,
            ['oubihihajar@gmail.com'],
            fail_silently=False,
        )
        
        return render(request, 'accounts/contact_success_u.html')
    else:
        return render(request, 'accounts/contact_u.html')

def about(request):
    return render(request, 'accounts/about.html')

def about_u(request):
    return render(request, 'accounts/about_u.html')

def AllEvents(request):
    if request.user.is_authenticated:
        print(f"Authenticated User: {request.user.username}")  # print username of authenticated user
        events = Event.objects.filter(organizer=request.user)
        print(f"Events: {events}")  # print queryset of events
        context = {
            'account': Account.objects.get(user=request.user),
            'events': events
        }
        return render(request, 'accounts/organizer_events.html', context)
    else:
        print("User is not authenticated.")  # print a message if user is not authenticated
        return redirect('login')


from django.shortcuts import get_object_or_404
def remove_ticket(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    event = order.event
    order.delete()
    # Redirect to the user's orders page
    return redirect('user_orders')



import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404

from django.urls import reverse


stripe.api_key = settings.STRIPE_SECRET_KEY

def payment(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        # Create the order
        order = Order.objects.create(
            user=request.user,
            event=event,
            total_amount=event.ticket_price,
            purchase_date=timezone.now()
        )

        # Add tickets to the order (if applicable)
        # Replace the following line with your logic to add the appropriate tickets to the order
        # order.tickets.add(event)

        # Update the payment status (if applicable)
        order.payment_status = 'complete'

        # Save the order
        order.save()

        # Retrieve the order details for the payment session
        order_price = int(order.total_amount * 100)  # Convert the ticket price to cents
        order_currency = 'MAD'  # Example: order currency (Moroccan dirhams)
        order_description = f"Ticket for the event: {event.title}"

        # Create the payment session with Stripe
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': order_currency,
                    'unit_amount': order_price,
                    'product_data': {
                        'name': order_description,
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
            metadata={
                'order_id': str(order.id)  # Set the order ID in the metadata
            }
        )

        # Redirect the user to the Stripe payment page
        return redirect(session.url)

    return render(request, 'accounts/payment.html', {'event': event})


def payment_success(request):
    # Retrieve the session_id from the request's GET parameters
    session_id = request.GET.get('session_id')
    print("Session ID:", session_id)  # Add this line to print the session ID

    if session_id:
        try:
            # Retrieve the session information from Stripe
            session = stripe.checkout.Session.retrieve(session_id)
            print("Stripe Session:", session)  # Add this line to print the Stripe session

            # Retrieve the order_id associated with the session from metadata
            order_id = session.metadata.get('order_id')
            print("Order ID:", order_id)  # Add this line to print the order ID

            # Update the payment status of the order in your order model
            order = Order.objects.get(pk=order_id)
            order.payment_status = 'complete'
            order.save()

            # Perform any other actions or notifications related to successful payment

            return render(request, 'accounts/payment_success.html')
        except Exception as e:
            # Handle errors when processing successful payment
            print("Error:", str(e))  # Add this line to print the error message
            return render(request, 'accounts/payment_error.html', {'error_message': str(e)})
    else:
        # Handle the case where session_id is not available
        return render(request, 'accounts/payment_error.html', {'error_message': 'Invalid session ID'})



def payment_cancel(request):
    # Traiter l'annulation de paiement
    return render(request, 'accounts/payment_cancel.html')




from django.db.models import Q
"""class EventListView(ListView):
    model = Event
    template_name = 'accounts/dashboard_user.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'events'
    ordering = ['date_time']
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Event.objects.filter(
                Q(location__icontains=query) & 
                Q(status='approved')
            )
        else:
            return Event.objects.filter(status='approved')"""


"""def event_list(request):
    search_query = request.GET.get('search')
    events = Event.objects.all()

    if search_query:
        events = events.filter(location__icontains=search_query)

    return render(request, 'event_list.html', {'events': events})
"""