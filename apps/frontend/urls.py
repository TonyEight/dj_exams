from django.conf.urls import url, include
from frontend.views import (
	HomeView,
	SubmissionCreateView,
	SubmissionReView,
	SubmissionPDFView
)


urlpatterns = [
	url(
		r'^$',
		HomeView.as_view(),
		name='home'
	),
	url(
		r'^exam/(?P<exam_pk>\d+)/submission/$',
		SubmissionCreateView.as_view(),
		name='exam-completion'
	),
	url(
		r'^submission/(?P<submission_id>[0-9a-z-]+)/$',
		SubmissionReView.as_view(),
		name='submission-review'
	),
	url(
		r'^submission/(?P<submission_id>[0-9a-z-]+)/pdf/$',
		SubmissionPDFView.as_view(),
		name='submission-review-pdf'
	),
]