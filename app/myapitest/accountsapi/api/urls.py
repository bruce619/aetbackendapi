from django.urls import path
from .views import (
    create_user,
    obtain_auth_token
)

urlpatterns = [
    path('create-user', create_user, name="create-user"),
    path('user/token', obtain_auth_token, name='auth'),
]