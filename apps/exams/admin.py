from django.contrib import admin
from exams.models import Question, Answer, Exam, ExamContext


class ExamContextInlines(admin.TabularInline):
    model = ExamContext
    extra = 2


class ExamAdmin(admin.ModelAdmin):
    inlines = [ExamContextInlines,]
    list_display = ['name', 'global_scale', 'scale',]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'label',]


class AnswerInlines(admin.TabularInline):
    model = Answer
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInlines,]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Exam, ExamAdmin)
