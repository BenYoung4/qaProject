from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .form import RegisterCustomerForm

CustomUser = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
        else:
            messages.error(request, 'Error during registration')
    else:
        form = RegisterCustomerForm()
        context = {'form': form}
        return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

def logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('login')
