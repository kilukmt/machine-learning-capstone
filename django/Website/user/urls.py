from django.conf.urls import url
from . import views

app_name = 'user'
urlpatterns = [
	# url(r'^$', views.UserView.as_view(), name='index'),
	url(r'^(?P<pk>[0-9]+)/$', views.UserView.as_view(), name='user'),
	url(r'^create_user/$', views.create_user, name='create_user'),
	url(r'^cu/$', views.process_new_user, name='process_new_user'),
]