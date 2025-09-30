from django.urls import path, include
from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('setup/',views.setup, name='setup'),
    path('quiz/',views.quiz, name='quiz'),
    path('results/',views.results, name='results'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings_view, name='settings'),
]