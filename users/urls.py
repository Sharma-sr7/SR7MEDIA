from django.urls import path
from .views import *


urlpatterns = [
    path('',login_page, name='login_url'),
    path('logout/',logout_page, name='logout_url'),
    path('register/',register_page, name='register_url'),
]
