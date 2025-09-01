from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserSignUpForm
from .models import Profile


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role')
            if role:
                Profile.objects.create(user=user, role=role)
            login(request, user)
            return redirect('home')
    else:
        form = UserSignUpForm()

    return render(request, 'registration/signup.html', {'form': form})