from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import User
from orders.models import Order
from .forms import UserRegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # UserProfile.objects.create(user = new_user)  
            login(request, new_user)
            return redirect('index') 
        
       
    else:
        form = UserRegisterForm()
    return render(request, 'user/signup.html', {
        'form': form
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Credentials')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', { 'form': form })

def logout_view(request):
    logout(request)
    return redirect('login')

def user_dashboard_view(request):
    user = request.user
    user_profile = user.profile
    print("Current User: ", user)
    print("Current Profile: ", user_profile)

    previous_orders = request.user.orders.filter(paid=True)
    return render(request, 'user/user-dashboard.html', {
        'user': user,
        'user_profile': user_profile,
        'previous_orders': previous_orders
    })

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST)
    else:
        user_form = UserUpdateForm()
        profile_form = ProfileUpdateForm()
    return render(request, 'user/profile-update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })