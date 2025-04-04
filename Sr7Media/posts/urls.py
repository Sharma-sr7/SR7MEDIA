from django.urls import path
from .views import *


urlpatterns = [
    path('',Home, name='home_url'),
    path('profile/<str:pk>/',profile, name='profile_url'),
    path('update/',update, name='update_url'),
    path('upload/',upload, name='upload_url'),
    path('like-post/',like_post, name='like_url'),
    path('follow/',follow, name='follow_url'),
    path('search/',search, name='search_url'),
    path('privacy/',privacy, name='privacy_url'),
    path('userposts/<str:pk>/',userposts,name='userposts_url'),
    path('delete/<str:pk>/',deletepost,name='delete_url'),
    path('load_comments/', load_comments, name='load_comments'),
    path('submit_comment/', submit_comment, name='submit_comment'),
    path('delete_account/', delete_account, name='delete_account'),

]
