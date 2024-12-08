from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, user_api_login

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', user_api_login, name='user_api_login'),
]
