from django.urls import path
from .views import RegisterUser, UserLogin, LogoutView, UserProfile
app_name = 'users'

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', UserProfile.as_view(), name='profile'),
    path('verify/<str:email>/<str:activation_key>/', RegisterUser.verify,  name='verify')
]
