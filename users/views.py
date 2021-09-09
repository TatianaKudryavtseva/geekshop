from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from django.contrib import messages
from django.views.generic.edit import CreateView
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from baskets.models import Basket
from users.models import User


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'title': 'GeekShop - Авторизация', 'form': form}
    return render(request, 'users/login.html', context)


class UserRegistrationView(CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserRegistrationView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Регистрация'
        return context


def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(instance=user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные изменены')
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=user)
    context = {'title': 'GeekShop - Профиль',
               'form': form,
               'baskets': Basket.objects.filter(user=user)}
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
