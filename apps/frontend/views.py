from django import forms
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, TemplateView, CreateView, DetailView
from easy_pdf.views import PDFTemplateView
from exams.models import Exam, Subject, Answer
from students.models import Submission

class HeaderContextMixin(View):
    def get_context_data(self, *args, **kwargs):
        subjects = [subject for subject in Subject.objects.all()\
                    if subject.exams.filter(is_published=True).count() > 0]
        context = super(HeaderContextMixin, self).get_context_data(
            *args,
            **kwargs
        )
        context.update({
            'subjects': subjects
        })
        return context


class HomeView(HeaderContextMixin, TemplateView):
    template_name = 'frontend/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(
            *args,
            **kwargs
        )
        context.update({
            'exams': Exam.objects.filter(is_published=True)
        })
        return context


class SubmissionCreateView(HeaderContextMixin, CreateView):
    model = Submission
    template_name = 'frontend/submission_completion.html'
    fields = [
        'first_name',
        'last_name',
        'email',
    ] 

    def get_context_data(self, *args, **kwargs):
        context = super(SubmissionCreateView, self).get_context_data(
            *args,
            **kwargs
        )
        context.update({
            'exam': Exam.objects.get(pk=self.kwargs['exam_pk'])
        })
        return context

    def get_success_url(self):
        return reverse_lazy(
            'submission-review',
            kwargs={'submission_id': self.object.id}
        )

    def _build_questions_fields(self):
        exam = Exam.objects.get(pk=self.kwargs['exam_pk'])
        questions_fields = {}
        for context in exam.examcontext_set.all():
            ANSWERS = [(answer.pk, answer.label) for answer in context.question.possible_answers.all()]
            questions_fields['question_' + str(context.question.pk)] = forms.MultipleChoiceField(choices=ANSWERS, widget=forms.CheckboxSelectMultiple())
        return questions_fields

    def get_form(self, *args, **kwargs):
        form = super(SubmissionCreateView, self).get_form(*args, **kwargs)
        fields = form.fields
        questions_fields = self._build_questions_fields()
        for key in questions_fields:
            if key in fields.keys():
                del questions_fields[key]
        fields.update(questions_fields)
        form.fields = fields
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.exam = Exam.objects.get(pk=self.kwargs['exam_pk'])
        self.object.save()
        for key, value in form.cleaned_data.items():
            if key.startswith('question_'):
                for pk in value:
                    self.object.replies.add(Answer.objects.get(pk=int(pk)))
        return redirect(self.get_success_url())


class SubmissionReView(HeaderContextMixin, DetailView):
    template_name = 'frontend/submission_review.html'
    model = Submission
    context_object_name = 'submission'

    def get_object(self):
        return Submission.objects.get(id=self.kwargs['submission_id'])

    def get_context_data(self, *args, **kwargs):
        context = super(SubmissionReView, self).get_context_data(
            *args,
            **kwargs
        )
        results = []
        for c in self.object.exam.examcontext_set.all():
            results.append(
                (
                    c.question,
                    self.object.result_per_question(c.question.pk),
                    c.scale
                )
            )
        context.update({
            'results_per_question': results
        })
        return context

class SubmissionPDFView(PDFTemplateView):
    template_name = 'frontend/submission_review_pdf.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SubmissionPDFView, self).get_context_data(
            *args,
            **kwargs
        )
        submission = Submission.objects.get(id=self.kwargs['submission_id'])
        results = []
        for c in submission.exam.examcontext_set.all():
            results.append(
                (
                    c.question,
                    submission.result_per_question(c.question.pk),
                    c.scale
                )
            )
        context.update({
            'submission': submission,
            'results_per_question': results
        })
        return context