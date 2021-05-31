from django.urls import path

from rest_api import views

urlpatterns = [
    path('users/', views.UserView.as_view(), name='rest_api-users'),
    path('users/<int:id>/', views.UserDetailView.as_view(), name='rest_api-user_detail'),
    path('example/', views.ExampleView.as_view(), name='rest_api-example'),
    path('async_users/', views.UserAsyncView.as_view(), name='rest_api-async_users'),
]