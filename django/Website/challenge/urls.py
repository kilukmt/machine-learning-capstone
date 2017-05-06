from django.conf.urls import url
from . import views

app_name = 'challenge'
urlpatterns = [
	# url(r'^$', views.UserView.as_view(), name='index'),
	url(r'^$', views.challenges_home, name='home'),
	url(r'^(?P<challenge_id>[0-9]+)/$', views.challenge_page, name='challenge'),
	url(r'^(?P<challenge_id>[0-9]+)/helpcomment/(((?P<comment_id>[0-9]+)/)*)$', views.help_comment, name='help_comment'),
	url(r'^(?P<challenge_id>[0-9]+)/submit/$', views.submit, name='submit'),
	url(r'^submit/$', views.process_submit, name='process_submit'),
	url(r'^helpcomment/(?P<comment_id>[0-9]+)/$', views.index_help_comment, name="comment"),
	url(r'^post_comment/$', views.process_help_comment, name='process_help_comment'),
	# url(r'^test(?P<challenge_id>[0-9]+)/$', views.test, name='test')
]
