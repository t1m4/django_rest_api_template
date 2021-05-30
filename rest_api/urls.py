from django.urls import path

from rest_api import views

urlpatterns = [
    path('users/', views.UserView.as_view(), name='rest_api-users'),
    path('async_users/', views.UserAsyncView.as_view(), name='rest_api-users'),
]