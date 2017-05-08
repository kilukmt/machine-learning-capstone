from django.conf.urls import url
from . import views

app_name = 'user'
urlpatterns = [
	url(r'^user_index/$', views.user_index, name='all_users'),
	url(r'^(?P<user_id>[0-9]+)/$', views.user, name='user'),
	url(r'^login/$', views.login, name='login'),
	url(r'^li/$', views.process_login, name='process_login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^create_user/$', views.create_user, name='create_user'),
	url(r'^cu/$', views.process_new_user, name='process_new_user'),
	url(r'^changepicture(?P<user_id>[0-9]+)/$', views.change_user_picture, name='change_user_picture'),
	url(r'^cp(?P<user_id>[0-9]+)/$', views.process_change_user_picture, name='process_change_user_picture'),
	url(r'^group(?P<group_id>[0-9]+)/$', views.group, name='group'),
	url(r'^groups/$', views.group_index, name='group_index'),
	url(r'^create_group/$', views.create_group, name='create_group'),
	url(r'^cg/$', views.process_new_group, name='process_new_group'),
	url(r'^join_group(?P<group_id>[0-9]+)/$', views.join_group, name='join_group'),
	url(r'^leave_group(?P<group_id>[0-9]+)/$', views.leave_group, name='leave_group'),
]