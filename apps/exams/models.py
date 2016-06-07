from django.db import models


class Question(models.Model):
    LANGUAGES = (
        ('python', 'Python'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('javascript', 'JavaScript'),
    )
    label = models.CharField(verbose_name='label', max_length=700)
    snippet = models.TextField(verbose_name='snippet', null=True, blank=True)
    snippet_language = models.CharField(
        verbose_name='snippet language',
        max_length=200,
        choices=LANGUAGES,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        self.snippet = self.snippet.strip()
        super(Question, self).save(*args, **kwargs)

    @property
    def correct_answers(self):
        return self._count_correct_answers()

    @property
    def list_correct_answers(self):
        return self._list_correct_answers()

    def _list_correct_answers(self):
        return [answer for answer in self.possible_answers.all()\
                if answer.is_correct]
    

    def _count_correct_answers(self):
        count = 0
        for answer in self.possible_answers.all():
            if answer.is_correct:
                count += 1
        return count


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        verbose_name='question',
        related_name='possible_answers'
    )
    label = models.CharField(verbose_name='label', max_length=700)
    is_correct = models.BooleanField(verbose_name='correct answer', default=1)

    def __str__(self):
        return self.label


class Subject(models.Model):
    label = models.CharField(verbose_name='label', max_length=700)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        self.label = self.label.upper()
        super(Subject, self).save(*args, **kwargs)


class Exam(models.Model):
    subject = models.ForeignKey(
        Subject,
        verbose_name='subject',
        related_name='exams',
        default=Subject.objects.all()[0].pk
    )
    is_published = models.BooleanField(verbose_name='is published', default=1)
    name = models.CharField(verbose_name='name', max_length=700)
    description = models.TextField(verbose_name='description')
    strict = models.BooleanField(verbose_name='stricted corretion', default=1)
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
