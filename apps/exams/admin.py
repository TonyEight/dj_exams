from django.contrib import admin
from exams.models import Question, Answer, Exam, ExamContext, Subject


class ExamContextInlines(admin.TabularInline):
    model = ExamContext
    extra = 2


class ExamAdmin(admin.ModelAdmin):
    inlines = [ExamContextInlines,]
    list_display = ['subject', 'name', 'strict', 'global_scale', 'scale',]
    list_display_links = ['name',]


class AnswerInlines(admin.TabularInline):
    model = Answer
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInlines,]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Subject)