from django.db import models
from django.conf import settings



class AIModel(models.Model):
    """Manages available Gemini versions (Flash, Pro, etc.)"""
    display_name = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100, help_text="The API string, e.g., 'gemini-1.5-flash'")
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name


class Topic(models.Model):
    """Predefined topics for the setup page (e.g., 'Decorators', 'Flexbox')"""
    language = models.CharField(max_length=50, help_text="e.g., python, css")
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['language', 'name']

    def __str__(self):
        return f"{self.language} - {self.name}"


class Quiz(models.Model):
    """Represents a generated quiz session"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quizzes')
    language = models.CharField(max_length=50)
    topic_description = models.CharField(max_length=255, help_text="The topic user asked for")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Metadata
    model_used = models.CharField(max_length=100, blank=True)
    total_questions = models.IntegerField(default=0)
    score = models.IntegerField(default=0, help_text="Score percentage")
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.language} ({self.difficulty}) - {self.user.email}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    # Stores the code block (optional)
    code_snippet = models.TextField(blank=True, null=True, help_text="Code context for the question")
    explanation = models.TextField(blank=True, help_text="AI explanation for the correct answer")
    
    def __str__(self):
        return self.text[:50]


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    """Tracks which option the user selected"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    
    # Store the specific AI explanation for *this* error here if needed
    error_explanation = models.TextField(blank=True)

    def __str__(self):
        status = "Correct" if self.is_correct else "Incorrect"
        return f"{status} answer for {self.question.id}"