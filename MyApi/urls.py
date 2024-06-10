from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('userregister/', views.registerUser, name='registerUser'),
    path('gettable/<str:pk>/', views.gettable, name='gettable'),
    path('getalltable/', views.getalltable, name='getalltable'),

    path('', views.index, name='index'),
    path('start_timer/<str:pk>/', views.start_timer, name='start_timer'),
    path('stop_timer/<str:pk>/', views.stop_timer, name='stop_timer'),
]
   