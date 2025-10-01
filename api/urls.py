from django.urls import path
from . import views

urlpatterns = [

    path('create/', views.create_quiz, name='create_quiz'),

    path('attempt/<int:attempt_id>/question/<int:question_number>/', views.process_question, name='process_question'),
    path('attempt/<int:attempt_id>/finish/', views.finish_quiz, name='finish_quiz'),
    path('results/<int:attempt_id>/', views.quiz_results, name='quiz_results'),

    path('generate-from-chat/', views.generate_from_chat, name='generate_from_chat'),
]