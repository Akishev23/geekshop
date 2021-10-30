from django.urls import path
from .views import RegisterUser, UserLogin, logout_user, UserProfile, verify

app_name = 'users'

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('profile/<int:pk>/', UserProfile.as_view(), name='profile'),
    path('verify/<str:email>/<str:activation_key>/', verify,  name='verify')
]
