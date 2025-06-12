from django.urls import path
from . import views

urlpatterns = [
    path('event/', views.track_event, name='track_event'),
    path('dashboard/', views.dashboard, name='dashboard'),
]