from django.urls import path, re_path
from user.views import RegisterView, CustomAuthToken, Logout, UserProfileViewSet

user_list = UserProfileViewSet.as_view({'get': 'list'})
userProfile_get_create = UserProfileViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('users/', user_list, name='users'),
    path('userprofile/', userProfile_get_create, name='create'),
    path('search', userProfile_get_create, name='get')
]