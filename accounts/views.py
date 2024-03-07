from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .form import RegisterCustomerForm

CustomUser = get_user_model()


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterCustomerForm
    success_url = 'login'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Registration successful')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error during registration')
        return super().form_invalid(form)


def login(request):
    if request.method == 'POST':
        return authenticate_user_and_login(request)
    return render(request, 'accounts/login.html')


def authenticate_user_and_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    authenticated_user = authenticate(request, username=username, password=password)
    if authenticated_user is not None:
        auth_login(request, authenticated_user)
        return redirect('home')
    else:
        messages.error(request, 'Invalid username or password')


class LogoutView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        messages.success(request, 'You have successfully logged out')
        return super().get(request, *args, **kwargs)
