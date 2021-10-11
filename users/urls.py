from django.urls import path
from django.views.decorators.cache import cache_page
from users.views import UserLoginView, UserRegistrationView, profile, UserLogoutView
from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login/', cache_page(3600)(UserLoginView.as_view()), name='login'),
    path('registration/', cache_page(3600)(UserRegistrationView.as_view()), name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', cache_page(3600)(UserLogoutView.as_view()), name='logout'),
    path('verify/<str:email>/<str:activation_key>/', cache_page(3600)(UserRegistrationView.verify), name='verify'),
]