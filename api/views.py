from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.core.paginator import Paginator
from main.views import get_user_from_session
from .utils import generate_quiz_from_ai, get_explanation_from_ai, parse_quiz_request_with_ai
from .models import Quiz, Question, Option, QuizAttempt, UserAnswer, Topic
import json





@transaction.atomic
def create_quiz(request):

    if request.method != 'POST':
        return redirect('home')

    user = get_user_from_session(request)
    if not user:
        return redirect('login')

    language = request.POST.get('language')
    level = request.POST.get('level')
    num_questions = int(request.POST.get('num_questions', 5))

    predefined_topics = request.POST.getlist('predefined_topics')
    custom_topics_str = request.POST.get('custom_topics', '')
    custom_topics = [topic.strip() for topic in custom_topics_str.split(',') if topic.strip()]
    
    all_topics = list(set(predefined_topics + custom_topics))
    
    if not all_topics:
        messages.error(request, "Please select or enter at least one topic.")
        return redirect('setup', language_slug=language)

    quiz_data = generate_quiz_from_ai(language, level, all_topics, num_questions)
    
    print("--- AI RESPONSE ---", quiz_data) 
    
    if 'error' in quiz_data or not quiz_data.get('questions'):
        messages.error(request, "Sorry, an error occurred while generating the quiz. Please try again.")
        return redirect('setup', language_slug=language)
        
    quiz = Quiz.objects.create(user=user, language=language, level=level, topics=", ".join(all_topics))

    for q_data in quiz_data['questions']:
        question = Question.objects.create(quiz=quiz, question_text=q_data['question_text'])
        for o_text in q_data['options']:
            is_correct = (o_text == q_data['correct_answer'])
            Option.objects.create(question=question, option_text=o_text, is_correct=is_correct)
    
    attempt = QuizAttempt.objects.create(quiz=quiz, user=user)

    return redirect('process_question', attempt_id=attempt.id, question_number=1)





def process_question(request, attempt_id, question_number):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')

    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=user)
    questions = attempt.quiz.questions.all().order_by('id')
    
    paginator = Paginator(questions, 1)
    page_obj = paginator.get_page(question_number)
    current_question = page_obj.object_list[0]
    total_questions = paginator.num_pages
    progress_percentage = (question_number / total_questions) * 100

    if request.method == 'POST':
        selected_option_id = request.POST.get('answer')
        is_correct = False
        selected_option = None

        if selected_option_id:
            selected_option = get_object_or_404(Option, id=selected_option_id)
            is_correct = selected_option.is_correct

        UserAnswer.objects.create(
            attempt=attempt,
            question=current_question,
            selected_option=selected_option,
            is_correct=is_correct
        )

        if page_obj.has_next():
            next_question_number = page_obj.next_page_number()
            return redirect('process_question', attempt_id=attempt.id, question_number=next_question_number)
        else:
            return redirect('finish_quiz', attempt_id=attempt.id)

    context = {
        'user': user,
        'attempt': attempt,
        'question': current_question,
        'question_number': question_number,
        'total_questions': total_questions,
        'progress_percentage': progress_percentage,
        'is_last_question': not page_obj.has_next(),
    }
    return render(request, 'quiz.html', context)





@transaction.atomic
def finish_quiz(request, attempt_id):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')

    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=user)
    
    total_questions = attempt.quiz.questions.count()
    correct_answers = attempt.answers.filter(is_correct=True).count()
    attempt.score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
    attempt.save()

    incorrect_answers = attempt.answers.filter(is_correct=False).select_related('question', 'selected_option')
    for answer in incorrect_answers:
        if answer.selected_option:
            correct_option = answer.question.get_correct_option()
            question_data = {
                'question_text': answer.question.question_text,
                'correct_answer': correct_option.option_text
            }
            explanation_data = get_explanation_from_ai(question_data, answer.selected_option.option_text)
            if 'explanation' in explanation_data:
                answer.explanation = explanation_data['explanation']
                answer.save()

    return redirect('quiz_results', attempt_id=attempt.id)





def quiz_results(request, attempt_id):
    user = get_user_from_session(request)
    if not user:
        return redirect('login')
    
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=user)
    return render(request, 'results.html', {'attempt': attempt, 'user': user})





@transaction.atomic
def generate_from_chat(request):
    if request.method == 'POST':
        user = get_user_from_session(request)
        if not user:
            return JsonResponse({'error': 'User not logged in.'}, status=401)

        data = json.loads(request.body)
        user_message = data.get('message')
        num_questions = data.get('num_questions')

        parsed_request = parse_quiz_request_with_ai(user_message, num_questions)
        if 'error' in parsed_request:
            return JsonResponse(parsed_request, status=400)

        language = parsed_request.get('language')
        topic = parsed_request.get('topic')
        
        quiz_data = generate_quiz_from_ai(language, 'intermediate', [topic], num_questions)
        if 'error' in quiz_data or not quiz_data.get('questions'):
            return JsonResponse({'error': 'Failed to generate the quiz from your request.'}, status=500)

        quiz = Quiz.objects.create(user=user, language=language, level='intermediate', topics=topic)
        for q_data in quiz_data['questions']:
            question = Question.objects.create(quiz=quiz, question_text=q_data['question_text'])
            for o_text in q_data['options']:
                is_correct = (o_text == q_data['correct_answer'])
                Option.objects.create(question=question, option_text=o_text, is_correct=is_correct)
        
        attempt = QuizAttempt.objects.create(quiz=quiz, user=user)

        start_url = f'/api/attempt/{attempt.id}/question/1/'
        return JsonResponse({'quiz_start_url': start_url})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)