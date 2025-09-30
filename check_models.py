import google.generativeai as genai
import os
from dotenv import load_dotenv

# This assumes your .env file is in the parent directory of 'backend'
# which is the project root: 'ai-quiz-project'
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

try:
    api_key = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    print("--- Finding available models for 'generateContent' ---")

    # List all models and filter for the ones we can use
    for m in genai.list_models():
      if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")

    print("\n--- Finished ---")

except KeyError:
    print("Error: GEMINI_API_KEY not found. Make sure your .env file is set up correctly.")
except Exception as e:
    print(f"An error occurred: {e}")