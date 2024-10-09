from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.EventList.as_view(), name='home'),
]