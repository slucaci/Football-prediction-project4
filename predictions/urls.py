from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.EventList.as_view(), name='home'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),
    path('about/', include('about.urls')),
    path('my-predictions/', views.user_predictions, name='user_predictions'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('event/<slug:slug>/edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('event/<slug:slug>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]