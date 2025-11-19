from django.contrib import admin
from .models import AIModel, Topic, Quiz, Question, Option, UserAnswer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    readonly_fields = ('question', 'selected_option', 'is_correct')
    extra = 0

class QuizAdmin(admin.ModelAdmin):
    list_display = ('language', 'topic_description', 'user', 'score', 'created_at')
    inlines = [UserAnswerInline]

admin.site.register(AIModel)
admin.site.register(Topic)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer)