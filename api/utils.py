import os
import json
import google.generativeai as genai
from django.conf import settings



try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest')
except AttributeError:
    print("GEMINI_API_KEY not found in settings. AI features will be disabled.")
    model = None



def parse_quiz_request_with_ai(user_text, num_questions):
    if not model:
        return {"error": "Gemini model is not configured."}

    prompt = f"""
    Analyze the user's request: "{user_text}"
    The user wants to generate a quiz with {num_questions} questions.

    Your task is to extract the specific programming language AND the main topic of the quiz.

    Provide the output ONLY in the following JSON format. Do not include any text, code blocks, or explanations before or after the JSON object.

    {{
      "language": "The programming language or technology (e.g., Python, CSS, JavaScript)",
      "topic": "The specific topic the user wants a quiz on (e.g., decorators, modern CSS layout)"
    }}
    """

    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        parsed_data = json.loads(cleaned_response)
        parsed_data['num_questions'] = num_questions
        return parsed_data
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error parsing user request with AI: {e}")
        return {"error": "Could not understand the quiz request."}




def generate_quiz_from_ai(language, level, topics, num_questions):
    if not model:
        return {"error": "Gemini model is not configured. Check API key."}

    prompt = f"""
    Generate a multiple-choice quiz with {num_questions} questions for a {level}-level programmer in {language}.
    The topics should be: {', '.join(topics)}.

    Provide the output ONLY in the following JSON format. Do not include any text, code blocks, or explanations before or after the JSON object.

    {{
      "questions": [
        {{
          "question_text": "Your question here",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "correct_answer": "The correct option text here"
        }}
      ]
    }}
    """

    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error decoding JSON or calling API: {e}")
        return {"error": "Failed to generate quiz."}




def get_explanation_from_ai(question_data, user_answer):
    if not model:
        return {"error": "Gemini model is not configured. Check API key."}

    prompt = f"""
    A user answered a quiz question incorrectly.
    The question was: "{question_data['question_text']}"
    The user's incorrect answer was: "{user_answer}"
    The correct answer is: "{question_data['correct_answer']}"

    In one single, brief sentence, explain why the user's answer is incorrect and why the correct answer is right. Be extremely concise.
    """
    try:
        response = model.generate_content(prompt)
        explanation = response.text.strip().replace('*', '')
        return {"explanation": explanation}
    except Exception as e:
        print(f"Error calling API for explanation: {e}")
        return {"error": "Failed to generate explanation."}