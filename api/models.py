from django.db import models
from main.models import User



class Topic(models.Model):

    name = models.CharField(max_length=100, unique=True)
    language = models.CharField(max_length=50, default='python')

    def __str__(self):
        return self.name




class Quiz(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    language = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    topics = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz for {self.user.email} on {self.topics}"




class Question(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()

    def __str__(self):
        return self.question_text[:50]

    def get_correct_option(self):
        return self.options.get(is_correct=True)




class Option(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.option_text} for question: {self.question.id}"




class QuizAttempt(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attempt {self.id} by {self.user.email} on {self.quiz.topics}"




class UserAnswer(models.Model):

    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Answer by {self.attempt.user.email} for question {self.question.id}"