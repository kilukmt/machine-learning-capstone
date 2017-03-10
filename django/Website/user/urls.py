from django.conf.urls import url
from . import views

app_name = 'user'
urlpatterns = [
	# url(r'^$', views.IndexView.as_view(), name='index'),
	# url(r'^(?P<pk>[0-9]+)/$', views.CreateUserView.as_view(), name='create_user'),
	url(r'^create_user/$', views.create_user, name='create_user'),
]