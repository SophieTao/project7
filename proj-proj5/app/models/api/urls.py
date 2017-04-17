from django.conf.urls import url
from . import views
from .views import CafeRetrieveUpdate, CommentRetrieveUpdate

urlpatterns = [
    url(r'^meals$', views.indexView,name='cafe_list'),
    url(r'^meals/create$', views.create_cafe, name='cafe-add'),
    url(r'^meals/(?P<pk>\d+)/delete$', views.delete_cafe, name='cafe-delete'),
    url(r'^meals/(?P<pk>[0-9]+)$', CafeRetrieveUpdate.as_view(), name="retrieve_update_cafes"),
    url(r'^allmeals$', views.retrieve_cafe_all,name='all_meals'),
    url(r'^recentmeals$', views.get_recent_meals,name='recent_meal'),


    url(r'^comments$', views.commentView, name='comment_list'),     
    url(r'^comments/create$', views.create_comment, name='comment-add'),
    url(r'^comments/(?P<pk>\d+)/delete$', views.delete_comment, name='comment-delete'),
    url(r'^comments/(?P<pk>[0-9]+)$', CommentRetrieveUpdate.as_view(), name="retrieve_update_comments"),
    url(r'^allcomments$', views.retrieve_comment_all,name='all_comments'),

    url(r'^$', views.profileView, name='home'),
    url(r'^profiles/create$', views.create_profile, name='profile-add'),    
    url(r'^profiles/delete/(?P<pk>\d+)$', views.delete_profile, name='profile-delete'),
    # url(r'^profiles/(?P<pk>[0-9]+)$', ProfileRetrieveUpdate.as_view(), name="retrieve_update_profiles"),
    url(r'^profiles/retrieve$', views.retrieve_profile, name='profile-retrieve'),
    url(r'^profiles/check$', views.check_dup, name='check_dup'),

    url(r'^auth/create$', views.createAuth, name="create_auth"),
    url(r'^auth/delete/(?P<authenticator>\w+)$', views.deleteAuth, name="delete_auth"),
    url(r'^auth/check$', views.checkAuth, name="check_auth"),
    # url(r'^auth/get/(?P<authenticator>\w+)$', views.getAuth, name="get_auth"),
    url(r'^auths$', views.authView, name="get_all_auth"),


]