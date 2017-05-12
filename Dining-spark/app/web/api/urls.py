from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^home/', views.home, name='home'),
	url(r'^meal/(?P<cafe_id>[0-9]+)/$', views.meal, name='meal'),
	url(r'^comment/(?P<comment_id>[0-9]+)/$', views.comment, name='comment'),
	url(r'^create_account/$', views.create_account, name='create_account'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^create_listing/$', views.create_listing, name='create_listing'),
	url(r'^search/$', views.search_listing, name='search_listing'),

]