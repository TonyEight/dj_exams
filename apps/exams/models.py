from django.db import models


class Question(models.Model):
    label = models.CharField(verbose_name='label', max_length=700)

    def __str__(self):
        return self.label


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        verbose_name='question',
        related_name='possible_answers'
    )
    label = models.CharField(verbose_name='label', max_length=700)
    is_correct = models.BooleanField(verbose_name='correct answer', default=0)

    def __str__(self):
        return self.label


class Exam(models.Model):
    name = models.CharField(verbose_name='name', max_length=700)
    questions = models.ManyToManyField(
        Question,
        verbose_name='questions',
        through='ExamContext'
    )

    def __str__(self):
        return self.name

    @property
    def global_scale(self):
        return self._get_global_scale()
    
    @property
    def scale(self):
        return self._get_normalized_scale()
    
    def _get_global_scale(self):
        global_scale = 0
        for question in self.questions.all():
            for context in question.examcontext_set.filter(exam=self):
                global_scale += context.scale
        return global_scale

    def _get_normalized_scale(self):
        try:
            normalized_scale = 20 / self.global_scale
        except:
            return 0
        else:
            return normalized_scale


class ExamContext(models.Model):
    exam = models.ForeignKey(
        Exam,
        verbose_name='exam'
    )
    question = models.ForeignKey(
        Question,
        verbose_name='question',
    )
    scale = models.PositiveIntegerField(verbose_name='scale', default=1)


    def __str__(self):
        return '%s (%d)' % (
            self.question,
            self.scale
        )
