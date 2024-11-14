from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from events import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Redirects to event list page on home URL
    path('login/', views.login_user, name='login'),  # URL for login page
    path('register/', views.register_user, name='register'),  # URL for registration page
    path('dashboard/', views.dashboard, name='dashboard'),  # URL for dashboard/home
    path('logout/', views.logout_user, name='logout'),  # URL for logout
    path('event_list/', views.event_list, name='event_list'),  # URL for event list page
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),  # URL for event details
    path('event/create/', views.event_create, name='event_create'),  # URL to create event
    path('event/<int:event_id>/update/', views.event_update, name='event_update'),  # URL to update event
    path('event/<int:event_id>/delete/', views.event_delete, name='event_delete'),  # URL to delete event
    path('event/<int:event_id>/register/', views.register_participant, name='register_participant'),  # URL for event registration
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
