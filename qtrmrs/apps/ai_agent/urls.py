from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_interface, name='chat_interface'),
    path('send/', views.process_chat_message, name='chat_process'),
]