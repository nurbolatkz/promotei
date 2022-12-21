from django.urls import path
from rest_framework import routers
from user.views import RegisterView, CustomAuthToken, Logout

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout')
]