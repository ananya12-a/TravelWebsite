"""
URL configuration for webapps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from travelwebsite import views


urlpatterns = [
    path('', views.login_action, name='home'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('my_profile', views.my_profile, name = 'my_profile'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    # path('trip', views.show_trip, name='show_trips'),
    path('trip/<int:id>', views.show_trips, name='show_trip'),
    # path('add_trip', views.add_trip, name='add_trip'),
    path('delete_trip/<int:trip_id>', views.delete_trip, name='delete_trip'),
    path('trip/delete_activity/<int:activity_id>', views.delete_activity, name='delete_activity'),
    path('trip/travelwebsite/get-trips', views.get_trip),
    path('edit-trip/travelwebsite/get-trips', views.get_trip),
    path('travelwebsite/add-activity/<int:trip_id>', views.add_activity, name='add_activity'),
    path('travelwebsite/delete-item/<int:item_id>', views.delete_trip, name='ajax-delete-trip'),
    path('edit-trip/<int:trip_id>',views.edit_trip, name='edit-trip'),
    path('travelwebsite/add-collaborator/<int:trip_id>', views.add_collaborator, name='add_collaborator'), 
    path('travelwebsite/add-collaborator/travelwebsite/get-trips', views.get_trip)
]