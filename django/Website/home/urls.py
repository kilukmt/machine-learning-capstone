from django.conf.urls import url
from . import views

app_name = 'home'
urlpatterns = [
	url(r'^create_user/$', views.home, name='home')
]