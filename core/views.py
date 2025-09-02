from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserSignUpForm, JobForm
from .models import Profile, Job


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

# A helper function to check if a user is a client
def is_client(user):
    return user.is_authenticated and user.profile.role == 'client'

@login_required
def job_list(request):
    jobs = Job.objects.filter(is_open=True).order_by('-created_at')
    return render(request, 'core/job_list.html', {'jobs': jobs})

@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'core/job_detail.html', {'job': job})

@login_required
@user_passes_test(is_client) # Only clients can access this view
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'core/job_create.html', {'form': form})