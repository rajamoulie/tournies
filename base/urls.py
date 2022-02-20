from unicodedata import name
from django.urls import path
from . import views 


urlpatterns = [
    path('user-login/', views.loginUser, name='user-login'),
    path('user-logout/', views.logoutUser, name='user-logout'),
    path('user-register/', views.registerUser, name='user-register'),
    path('user-profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('', views.home, name='home'),

    #Tourney
    path('tourney/<str:pk>/', views.tourney, name='tourney'),
    path('create-tourney/', views.createTourney, name='create-tourney'),
    path('update-tourney/<str:pk>/', views.updateTourney, name='update-tourney'),
    path('delete-tourney/<str:pk>/', views.deleteTourney, name='delete-tourney'),

    #Message
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),

    path('update-user/', views.updateUser, name='update-user'),
]