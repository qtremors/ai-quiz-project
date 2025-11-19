QUIZ_GENERATION_PROMPT = """
You are an expert technical interviewer.
Generate a multiple-choice quiz for a {level}-level programmer in {language}.
The specific topic is: {topic}.

Constraints:
1. Generate exactly {num_questions} questions.
2. {code_instruction}
3. Provide 4 options for each question.
4. Indicate the correct option.
5. Provide a brief explanation.

Output Format (Strict JSON):
{{
  "questions": [
    {{
      "text": "The question text here (do not include the code here)",
      "code_snippet": "def example():\\n    return 'Optional code here'", 
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A", 
      "explanation": "Why this is correct."
    }}
  ]
}}
"""





EXPLANATION_PROMPT = """
A user answered a quiz question incorrectly.
Question: "{question_text}"
User Answer: "{user_answer}"
Correct Answer: "{correct_answer}"

Task:
Explain briefly (in 2 sentences max) why the user's answer is wrong and why the correct answer is right.
Be encouraging but technically precise.
"""





INTENT_PARSING_PROMPT = """
Analyze the user's request: "{user_message}"

Extract the following parameters to generate a coding quiz:
1. Language (e.g., Python, JavaScript, SQL). If implied, infer it. Defaults to "General Programming".
2. Topic (e.g., Decorators, React Hooks). If general, use "General Knowledge".
3. Difficulty (Beginner, Intermediate, Expert). Default to Intermediate.
4. Count (Number of questions). Default to 5. Max 10.

Output ONLY valid JSON in this format:
{{
  "language": "Python",
  "topic": "Decorators",
  "level": "Expert",
  "count": 5
}}
"""