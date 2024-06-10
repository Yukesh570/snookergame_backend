from django.urls import path
from . import views

urlpatterns = [
    path('userregister/', views.registerUser, name='registerUser'),
    path('gettable/<str:pk>/', views.gettable, name='gettable'),

]
