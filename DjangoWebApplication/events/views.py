from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Event
from django.views.generic import ListView
from django.db.models import Q
from django.utils.decorators import method_decorator



# Create your views here.

class EventDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = 'events/dashboard.html'
    context_object_name = 'events'

    def test_func(self):
        return self.request.user.is_superuser


def organizer_check(user):
    return user.profile.type_user == 'organizer'

class OrganizerEventListView(user_passes_test(organizer_check, login_url='login'), ListView):
    model = Event
    template_name = 'events/organizer_event_list.html'

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

    @method_decorator(user_passes_test(organizer_check, login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class EventCreateView(user_passes_test(organizer_check, login_url='login'), CreateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['title', 'description', 'location', 'date_time', 'ticket_price', 'image']

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

class EventUpdateView(user_passes_test(organizer_check, login_url='login'), UpdateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['title', 'description', 'location', 'date_time', 'ticket_price', 'image']

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

class EventDeleteView(user_passes_test(organizer_check, login_url='login'), DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('organizer_event_list')

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

from django.views.generic import ListView
from .models import Event

class EventListView(ListView):
    model = Event
    template_name = 'events/home.html'  # <app>/<model>_<viewtype>.html
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
            return Event.objects.filter(status='approved')


class UserEventListView(ListView):
    model = Event
    template_name = 'events/user_events.html' 
    context_object_name = 'events'
    ordering = ['-date_time'] 
    paginate_by = 5
