from django.conf.urls import url
from . import views

app_name = 'challenge'
urlpatterns = [
	# url(r'^$', views.UserView.as_view(), name='index'),
	url(r'^(?P<challenge_id>[0-9]+)/$', views.challenge_page, name='challenge'),
	# url(r'^test(?P<challenge_id>[0-9]+)/$', views.test, name='test')
]
