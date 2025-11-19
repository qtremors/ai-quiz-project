import json
import logging
from .client import get_gemini_client
from .prompts import QUIZ_GENERATION_PROMPT, EXPLANATION_PROMPT, INTENT_PARSING_PROMPT

logger = logging.getLogger(__name__)

class QuizGenerator:
    """
    Service class to handle AI interactions for Quizzes.
    """
    
    def __init__(self, model_name='gemini-flash-lite-latest'):
        self.genai = get_gemini_client()
        self.model = self.genai.GenerativeModel(model_name)

    def generate_quiz(self, language, topic, level, num_questions=5, include_code=False):
        """
        Generates a structured quiz using Gemini.
        """
        # Dynamic instruction based on user choice
        if include_code:
            code_instruction = "Each question MUST include a relevant code snippet that the user must analyze to answer."
        else:
            code_instruction = "Questions should be conceptual. Do NOT include long code snippets."

        prompt = QUIZ_GENERATION_PROMPT.format(
            language=language,
            topic=topic,
            level=level,
            num_questions=num_questions,
            code_instruction=code_instruction
        )

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            quiz_data = json.loads(response.text)
            return quiz_data.get('questions', [])

        except Exception as e:
            logger.error(f"AI Generation Error: {e}")
            return []

    def generate_explanation(self, question_text, user_answer, correct_answer):
        """
        Generates a concise explanation for why the user was wrong.
        """
        prompt = f"""
        Context: A coding quiz.
        Question: "{question_text}"
        User's Wrong Answer: "{user_answer}"
        Correct Answer: "{correct_answer}"
        
        Task: Explain in 2 sentences why the user's answer is incorrect and why the correct answer is right. 
        Address the user directly ("You selected...").
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return "Unable to generate explanation at this moment."
        


    def parse_intent(self, user_message):
        """
        Converts natural language into structured quiz parameters.
        """
        prompt = INTENT_PARSING_PROMPT.format(user_message=user_message)
        
        try:
            response = self.model.generate_content(
                prompt, 
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Intent Parsing Error: {e}")
            # Fallback defaults
            return {
                "language": "General",
                "topic": "Random",
                "level": "Intermediate",
                "count": 5
            }