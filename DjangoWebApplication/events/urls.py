from django.urls import path
from . import views
from .views import EventDashboardView
from .views import OrganizerEventListView, EventCreateView, EventUpdateView, EventDeleteView, UserEventListView


urlpatterns = [
    path('events/', views.events, name='events'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/update/', views.update_event, name='update_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('dashboard/', EventDashboardView.as_view(), name='event-dashboard'),
    path('organizer/events/', OrganizerEventListView.as_view(), name='organizer_event_list'),
    path('organizer/events/new/', EventCreateView.as_view(), name='event_new'),
    path('organizer/events/<int:pk>/edit/', EventUpdateView.as_view(), name='event_edit'),
    path('organizer/events/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('user_events/', UserEventListView.as_view(), name='user-events'),
]
