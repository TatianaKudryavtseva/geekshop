from django.urls import path

from users.views import UserLoginView, UserRegistrationView, UserProfileView, UserLogoutView
from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<str:activation_key>/', UserRegistrationView.verify, name='verify'),
]