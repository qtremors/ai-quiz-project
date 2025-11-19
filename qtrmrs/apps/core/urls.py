from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('languages/', views.languages_list, name='languages_list'),
]