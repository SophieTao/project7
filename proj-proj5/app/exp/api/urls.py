from django.conf.urls import include, url
from django.contrib import admin
from . import views 

urlpatterns = [
	url(r'^home/$', views.home,name='home'),
	url(r'^meal/(?P<cafe_id>[0-9]+)/$', views.meal, name='meal'),
	url(r'^comment/(?P<comment_id>[0-9]+)/$', views.comment, name='comment'),
	# url(r'^profile/(?P<profile_id>[0-9]+)/$', views.profile, name='profile'),
	url(r'^profile/check$', views.check_dup, name='check_dup'),
	url(r'^login$', views.login, name='login'),
	url(r'^logout/(?P<authenticator>\w+)$', views.logout, name='logout'),
	url(r'^create_account$', views.create_account, name='create_account'),
    url(r'^expiredAuth/delete$', views.delete_expired_auth, name='delete_expired_auth'),
    url(r'^listing/create$', views.create_listing, name='create_listing'),		
    url(r'^auth/check$', views.check_auth, name='check_auth'),
    url(r'^auth/create$', views.create_auth, name='create_auth'),
    url(r'^search', views.search_listing, name='search_listing')

]
  
