from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.http import HttpResponse
from .services import QuizGenerator
from apps.quizzes.models import Quiz, Question, Option

@login_required
def chat_interface(request):
    """Renders the chat page."""
    return render(request, 'ai_agent/chat.html')

@login_required
@require_http_methods(["POST"])
def process_chat_message(request):
    """
    1. Receives user message.
    2. Parses intent (Language/Topic/Level).
    3. Generates Quiz.
    4. Redirects to Player.
    """
    user_message = request.POST.get('message', '')
    
    if not user_message.strip():
        return HttpResponse("Please type something.", status=400)

    generator = QuizGenerator()
    
    # 1. Parse Intent (What does the user want?)
    params = generator.parse_intent(user_message)
    
    # 2. Generate Content based on parsed params
    questions_data = generator.generate_quiz(
        language=params.get('language'),
        topic=params.get('topic'),
        level=params.get('level'),
        num_questions=params.get('count', 5)
    )

    if not questions_data:
        return render(request, 'components/chat_error.html', {
            'message': "I couldn't generate a quiz for that. Try being more specific."
        })

    # 3. Save to DB
    with transaction.atomic():
        quiz = Quiz.objects.create(
            user=request.user,
            language=params.get('language'),
            topic_description=f"{params['language']}: {params['topic']}",
            difficulty=params.get('level').lower(),
            total_questions=len(questions_data),
            model_used="Chat Agent"
        )

        for q_data in questions_data:
            question = Question.objects.create(
                quiz=quiz,
                text=q_data['text'],
                explanation=q_data.get('explanation', '')
            )
            
            for opt_text in q_data['options']:
                Option.objects.create(
                    question=question,
                    text=opt_text,
                    is_correct=(opt_text == q_data['correct_answer'])
                )

    # 4. Redirect to Player
    response = HttpResponse()
    response['HX-Redirect'] = f"/quiz/play/{quiz.id}/"
    return response