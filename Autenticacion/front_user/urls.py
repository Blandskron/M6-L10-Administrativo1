from django.urls import path
from . import views

app_name = 'front_user'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_user, name='register_user'),
    path('users/', views.list_users, name='list_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:user_id>/', views.detail_user, name='detail_user'),
    path('users/<int:user_id>/update/', views.update_user, name='update_user'),
]
