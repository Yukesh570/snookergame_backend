from django.urls import path
from . import views , python ,timer
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('userregister/', views.registerUser, name='registerUser'),
    path('registerTable/', views.registerTable, name='registerTable '),

    path('updatetable/<str:pk>/', views.updatetable, name='updatetable'),
    path('chooseGame/<str:pk>/', views.chooseGame, name='chooseGame'),
    path('video_feed/', views.video_feed, name='video_feed'),

    path('gettable/<str:pk>/', views.gettable, name='gettable'),
    path('getalltable/', views.getalltable, name='getalltable'),
    path('timer/<str:pk>/', timer.timer, name='timer'),

    path('index/', views.index, name='index'),
    path('start_timer/<str:pk>/', views.start_timer, name='start_timer'),
    path('stop_timer/<str:pk>/', views.stop_timer, name='stop_timer'),
    path('background_run/<int:pk>/<int:pk1>/', python.background_run, name='video_stream'),
    #//
    path('video_feed/<int:pk>/', python.video_feed, name='video_feed'),
    #//
    path('game_start/<int:pk>/', python.background_run, name='video_stream'),

    path('botton/<int:pk>/', python.botton, name='botton'),

]
   