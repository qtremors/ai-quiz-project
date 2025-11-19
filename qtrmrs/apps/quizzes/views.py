from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Quiz, Question, Option, UserAnswer
from apps.ai_agent.services import QuizGenerator

# ==========================================
# 1. QUIZ SETUP & CREATION
# ==========================================

@login_required
def quiz_setup(request):
    """Renders the quiz configuration page."""
    # Capture URL param e.g. /quiz/setup/?language=python
    initial_lang = request.GET.get('language', '')
    return render(request, 'quizzes/setup.html', {'initial_lang': initial_lang})

@login_required
@require_http_methods(["POST"])
def create_quiz(request):
    topic = request.POST.get('topic')
    
    # --- Handle Custom Language Logic ---
    lang_select = request.POST.get('language_select')
    custom_lang = request.POST.get('custom_language')
    
    # If custom_lang has text, USE IT. Else, use dropdown.
    language = custom_lang.strip() if custom_lang and custom_lang.strip() else lang_select
    
    level = request.POST.get('level', 'intermediate')
    num_questions = int(request.POST.get('num_questions', 5))
    include_code = request.POST.get('include_code') == 'on'
    
    generator = QuizGenerator()
    
    # Pass the new arguments
    questions_data = generator.generate_quiz(
        language=language, 
        topic=topic, 
        level=level, 
        num_questions=num_questions,
        include_code=include_code
    )

    if not questions_data:
        return render(request, 'components/error_alert.html', {
            'message': "AI failed to generate. Try again."
        })

    with transaction.atomic():
        quiz = Quiz.objects.create(
            user=request.user,
            language=language,
            topic_description=f"{language}: {topic}",
            difficulty=level,
            total_questions=len(questions_data),
            model_used=generator.model.model_name
        )

        for q_data in questions_data:
            question = Question.objects.create(
                quiz=quiz,
                text=q_data['text'],
                code_snippet=q_data.get('code_snippet', ''),
                explanation=q_data.get('explanation', '')
            )
            for opt_text in q_data['options']:
                Option.objects.create(
                    question=question,
                    text=opt_text,
                    is_correct=(opt_text == q_data['correct_answer'])
                )

    response = HttpResponse()
    response['HX-Redirect'] = f"/quiz/play/{quiz.id}/"
    return response


# ==========================================
# 2. CLASSIC EXAM PLAYER
# ==========================================

@login_required
def quiz_player(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user)
    
    answered_ids = quiz.answers.values_list('question_id', flat=True)
    current_question = quiz.questions.exclude(id__in=answered_ids).first()

    if not current_question:
        return redirect('quiz_results', quiz_id=quiz.id)

    total_qs = quiz.questions.count()
    # Avoid division by zero
    progress = (len(answered_ids) / total_qs * 100) if total_qs > 0 else 0

    return render(request, 'quizzes/player.html', {
        'quiz': quiz,
        'current_question': current_question,
        'progress': progress,
        'is_last': (len(answered_ids) + 1 == total_qs)
    })

@login_required
@require_http_methods(["POST"])
def submit_answer(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user)
    question = get_object_or_404(Question, id=question_id, quiz=quiz)
    
    selected_option_id = request.POST.get('option')
    action = request.POST.get('action')

    if action == 'skip' or not selected_option_id:
        UserAnswer.objects.create(quiz=quiz, question=question, selected_option=None, is_correct=False)
    else:
        selected_option = get_object_or_404(Option, id=selected_option_id, question=question)
        is_correct = selected_option.is_correct
        UserAnswer.objects.create(
            quiz=quiz, question=question, selected_option=selected_option, is_correct=is_correct
        )
        if is_correct:
            quiz.score += (100 / quiz.total_questions)
            quiz.save()

    # Get next question
    answered_ids = quiz.answers.values_list('question_id', flat=True)
    next_q = quiz.questions.exclude(id__in=answered_ids).first()

    if not next_q:
        response = HttpResponse()
        response['HX-Redirect'] = f"/quiz/results/{quiz.id}/"
        return response

    return render(request, 'quizzes/partials/question_card.html', {
        'quiz': quiz,
        'question': next_q,
        'progress': (len(answered_ids) / quiz.questions.count()) * 100,
        'is_last': (len(answered_ids) + 1 == quiz.questions.count())
    })

@login_required
def quiz_results(request, quiz_id):
    """Renders the results page."""
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user)
    user_answers = UserAnswer.objects.filter(quiz=quiz).select_related('question', 'selected_option')
    
    correct_count = user_answers.filter(is_correct=True).count()
    skipped_count = user_answers.filter(selected_option__isnull=True).count()
    wrong_count = quiz.total_questions - correct_count - skipped_count
    
    # Check if any explanations generated yet
    has_explanations = user_answers.exclude(error_explanation='').exists()

    return render(request, 'quizzes/results.html', {
        'quiz': quiz,
        'user_answers': user_answers,
        'score_percent': int(quiz.score),
        'correct': correct_count,
        'skipped': skipped_count,
        'wrong': wrong_count,
        'has_explanations': has_explanations
    })

@login_required
def generate_all_explanations(request, quiz_id):
    """
    HTMX View: 
    1. Finds ALL wrong/skipped answers.
    2. Generates AI text for them in a batch (loop).
    3. Re-renders the answer list part of the page with explanations included.
    """
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user)
    
    # Filter for wrong or skipped answers that don't have an explanation yet
    # (is_correct=False covers both Wrong and Skipped)
    answers_needing_help = UserAnswer.objects.filter(
        quiz=quiz, 
        is_correct=False, 
        error_explanation=''
    ).select_related('question', 'selected_option')
    
    generator = QuizGenerator()
    
    for ans in answers_needing_help:
        correct_opt = ans.question.options.filter(is_correct=True).first()
        user_text = ans.selected_option.text if ans.selected_option else "Skipped"
        
        explanation = generator.generate_explanation(
            question_text=ans.question.text,
            user_answer=user_text,
            correct_answer=correct_opt.text
        )
        ans.error_explanation = explanation
        ans.save()
    
    # Re-fetch all answers to render the list again
    user_answers = UserAnswer.objects.filter(quiz=quiz).select_related('question', 'selected_option')
    
    # We render a partial template that just contains the list loop
    return render(request, 'quizzes/partials/results_list.html', {'user_answers': user_answers})