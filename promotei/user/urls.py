from django.urls import path
from rest_framework import routers
from user.views import RegisterView, CustomAuthToken, Logout, UserProfileViewSet

user_list = UserProfileViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('users/', user_list, name='users'),
    #path('categories/<int:pk>', category_detail, name='category_detail'),
]