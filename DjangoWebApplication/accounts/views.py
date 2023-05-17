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


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        account_form = AccountRegisterForm(request.POST)  # changed from profile_form to account_form
        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save()
            account = account_form.save(commit=False)  # changed from profile to account
            account.user = user
            account.save()
            print("Register view called")  # Add this line to print a message
        
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
        else:
            messages.error(request, f'Please correct the error below.')
    else:
        user_form = UserRegisterForm()
        account_form = AccountRegisterForm()  # changed from profile_form to account_form
    return render(request, 'accounts/register.html', {'user_form': user_form, 'account_form': account_form})  # changed from 'profile_form' to 'account_form'


from django.contrib.auth.decorators import user_passes_test


def user_check(user):
    return Account.objects.get(user=user).user_type == 'user'  # changed from Profile to Account

def organizer_check(user):
    return Account.objects.get(user=user).user_type == 'organizer'  # changed from Profile to Account

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
    else:
        return render(request, 'accounts/login.html')

@user_passes_test(user_check, login_url='login')
def user_profile(request):
    account = Account.objects.get(user=request.user)  # changed from profile to account
    return render(request, 'accounts/user_profile.html', {'account': account})  # changed from 'profile' to 'account'

@user_passes_test(organizer_check, login_url='login')
def organizer_profile(request):
    account = Account.objects.get(user=request.user)  # changed from profile to account
    return render(request, 'accounts/organizer_profile.html', {'account': account})  # changed from 'profile' to 'account'


def logout_view(request):
    logout(request)
    return redirect('home')

    

@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        account_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user.account)

        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        account_form = AccountUpdateForm(instance=request.user.account)

    context = {
        'user_form': user_form,
        'account_form': account_form
    }

    return render(request, 'accounts/profile_update.html', context)

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