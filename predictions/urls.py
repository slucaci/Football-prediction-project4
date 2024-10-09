from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.EventList.as_view(), name='home'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),
    path('about/', include('about.urls')),
]