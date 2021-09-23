from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic.edit import UpdateView, FormView
from django.urls import reverse_lazy, reverse
from common.view import CommonContextMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from baskets.models import Basket
from users.models import User, UserProfile
from users.forms import UserProfileEditForm


class UserLoginView(CommonContextMixin, LoginView):
    title = 'GeekShop - Авторизация'
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('users:profile')


class UserRegistrationView(CommonContextMixin, SuccessMessageMixin, FormView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    success_message = f'Вы успешно зарегестрировались! Письмо с подтверждением регистрации отправлено на почту'
    title = 'GeekShop - Регистрация'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_mail(user):
                messages.success(request, f'Вы успешно зарегестрировались! '
                                          f'Письмо с подтверждением регистрации отправлено на почту')
                return redirect(self.success_url)
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    def send_verify_mail(self, user):
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        title = f'Подтверждение учетной записи {user.username}'
        message = f'Для подтверждения регистрации {user.username} на сайте {settings.DOMAIN_NAME} '\
                  f'пройдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

        return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user.activation_key == activation_key and not user.is_activation_key_expired():
                user.is_active = True
                user.save()
                return render(self, 'users/verification.html')
            else:
                print(f'error activation user: {user.username}')
                return render(self, 'users/verification.html')
        except Exception as err:
            print(f'error activation user: {err.args}')
            return HttpResponseRedirect(reverse('index'))


# class UserProfileView(CommonContextMixin, UpdateView):
#    model = User
#    template_name = 'users/profile.html'
#    form_class = UserProfileForm
#    title = 'GeekShop - Профиль'
#
#    def get_success_url(self):
#        return reverse_lazy('users:profile', args=(self.object.id,))
#
#    def get_context_data(self, **kwargs):
#        context = super(UserProfileView, self).get_context_data(**kwargs)
#        context['baskets'] = Basket.objects.filter(user=self.object)
#        return context


@transaction.atomic
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)

    context = {
        'form': form,
        'profile_form': profile_form,
        'title': 'GeekShop - Профиль',
        'baskets': Basket.objects.filter(user=request.user), }

    return render(request, 'users/profile.html', context)


class UserLogoutView(LogoutView):
    template_name = 'products/index.html'
