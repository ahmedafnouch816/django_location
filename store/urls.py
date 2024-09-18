from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    path('home/', views.home_view, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('vehicules/add/', views.add_vehicule, name='add_vehicule'),
    path('update_vehicule/<int:id>/', views.update_vehicule, name='update_vehicule'),
    path('list_vehicules/', views.list_vehicules, name='list_vehicules'),
    path('delete_vehicule/<int:id>/', views.delete_vehicule, name='delete_vehicule'),  # New URL pattern

    
    #client
    
    path('clients/', views.list_clients, name='list_clients'),
    path('clients/add/', views.add_client, name='add_client'),
    path('clients/<int:id>/update/', views.update_client, name='update_client'),    
    path('clients/delete/<int:id>/', views.delete_client, name='delete_client'),

    
    path('reserved-vehicles/', views.reserved_vehicles_list, name='reserved_vehicles_list'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
