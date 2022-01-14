from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('users/login/', LoginAPIView.as_view()),
    path('user', UserRetrieveAPIView.as_view()),
]