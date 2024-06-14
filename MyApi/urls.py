from django.urls import path,include
from . import views , python
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('userregister/', views.registerUser, name='registerUser'),
    path('registerTable/', views.registerTable, name='registerTable '),

    path('gettable/<str:pk>/', views.gettable, name='gettable'),
    path('getalltable/', views.getalltable, name='getalltable'),

    # path('start/<str:pk>/', python.index, name='index'),
    path('start_timer/<str:pk>/', views.start_timer, name='start_timer'),
    path('stop_timer/<str:pk>/', views.stop_timer, name='stop_timer'),
    path('video_stream/<int:pk>/', python.video_stream, name='video_stream'),

]
   