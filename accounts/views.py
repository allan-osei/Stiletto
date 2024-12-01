from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

from .forms import SignUpForm, LogInForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()  
        print("h") 
    return render(request, 'accounts/sign-up.html', {'form': form})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid email or password.")
        else:
            print(form.errors)
    else:
        form = LogInForm()

    return render(request, 'accounts/sign-in.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect(reverse('accounts:login'))