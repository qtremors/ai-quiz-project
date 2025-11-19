import google.generativeai as genai
from django.conf import settings

def get_gemini_client():

    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
    
    genai.configure(api_key=api_key)
    return genai