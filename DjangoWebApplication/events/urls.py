from django.urls import path
from . import views
from .views import EventDashboardView
from .views import  EventCreateView, EventUpdateView, EventDeleteView, UserEventListView
from .views import OrganizerEventListView


urlpatterns = [
    #path('events/', views.event, name='events'),
    #path('events/create/', views.create_event, name='create_event'),
    #path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    #path('events/<int:event_id>/update/', views.update_event, name='update_event'),
    #path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('dashboard/', EventDashboardView.as_view(), name='event-dashboard'),
    path('organizer/events/', views.OrganizerEventListView, name='organizer_event_list'),
    path('organizer/events/new/', views.EventCreateView, name='event_new'),
    path('organizer/events/<int:pk>/edit/', views.EventUpdateView, name='event_edit'),
    path('organizer/events/<int:pk>/delete/', views.EventDeleteView, name='event_delete'),
    path('user_events/', UserEventListView.as_view(), name='user-events'),
]
