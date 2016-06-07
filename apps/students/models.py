import uuid
from django.db import models
from exams.models import Exam, Answer


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(verbose_name='first name', max_length=300)
    last_name = models.CharField(verbose_name='last name', max_length=350)
    email = models.EmailField(verbose_name='email')
    submitted_at = models.DateTimeField(
        verbose_name='submitted at',
        auto_now_add=True,
        editable=False
    )
    exam = models.ForeignKey(
        Exam,
        verbose_name='exam',
        related_name='submissions'
    )
    replies = models.ManyToManyField(
        Answer,
        verbose_name='replies',
        editable=False
    )

    def __str__(self):
        return '%s | %s %s (%s)' % (
            self.exam,
            self.first_name,
            self.last_name,
            self.email
        )

    @property
    def student(self):
        return '%s %s (%s)' % (
            self.first_name,
            self.last_name,
            self.email
        )

    @property
    def result(self):
        per_question = []
        for context in self.exam.examcontext_set.all():
            per_question.append(self.result_per_question(context.question.pk))
        global_scale = 0
        for value in per_question:
            global_scale += value
        return global_scale

    def result_per_question(self, question_pk):
        context = self.exam.examcontext_set.get(question__pk=question_pk)
        q = context.question
        scale = 0
        if self.exam.strict:
            perfect = True
            for a in self.replies.filter(question__pk=question_pk):
                if a not in q.list_correct_answers:
                    perfect = False
            if perfect:
                scale = context.scale
            else:
                scale = 0
        else:
            scale = 0
            partial_pts = context.scale / q.correct_answers
            for a in q.list_correct_answers:
                if a in self.replies.all():
                    scale += partial_pts
        return scale    

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.upper()
        super(Submission, self).save(*args, **kwargs)
