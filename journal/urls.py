from django.urls import path
from . import views
from . import profile_views

app_name = 'journal'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('new-entry/', views.new_entry, name='new_entry'),
    path('history/', views.history, name='history'),
    path('api/mood-data/', views.mood_data_api, name='mood_data_api'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/mark-read/<int:pk>/', views.mark_notification_read, name='mark_notification_read'),
    path('profile/', profile_views.profile, name='profile'),
    path('profile/edit/', profile_views.edit_profile, name='edit_profile'),
    path('profile/change-password/', profile_views.change_password, name='change_password'),
]
