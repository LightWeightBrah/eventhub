from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event-list'),
    path('welcome/', views.welcome_view, name='events-welcome'),
    path('about/', views.about_view, name='events-about'),
    path('event/<slug:slug>/', views.event_detail, name='event-detail'),
    path('category/<slug:category_slug>/', views.events_by_category, name='events-by-category'),
]
