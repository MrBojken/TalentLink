from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserSignUpForm, JobForm, ProposalForm
from .models import Profile, Job, Proposal


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


# A helper function to check if a user is a freelancer
def is_freelancer(user):
    return user.is_authenticated and user.profile.role == 'freelancer'


@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    # Check if a proposal already exists for this user/job combination
    existing_proposal = Proposal.objects.filter(job=job, freelancer=request.user).first()

    is_freelancer_user = is_freelancer(request.user)
    is_client_owner = is_client(request.user) and job.client == request.user

    # Handle proposal submission for freelancers
    if request.method == 'POST' and is_freelancer_user:
        form = ProposalForm(request.POST)
        if form.is_valid() and not existing_proposal:
            proposal = form.save(commit=False)
            proposal.job = job
            proposal.freelancer = request.user
            proposal.save()
            return redirect('job_detail', pk=job.pk)

    # Set the form for the template
    form = ProposalForm()

    context = {
        'job': job,
        'form': form,
        'existing_proposal': existing_proposal,
        'is_client_owner': is_client_owner,
        'is_freelancer_user': is_freelancer_user,
    }
    return render(request, 'core/job_detail.html', context)


@login_required
def dashboard(request):
    if request.user.profile.role == 'client':
        # Get jobs posted by the client
        jobs = request.user.posted_jobs.all().order_by('-created_at')
        return render(request, 'core/client_dashboard.html', {'jobs': jobs})
    else: # Freelancer
        # Get proposals submitted by the freelancer
        proposals = request.user.proposals.all().order_by('-created_at')
        return render(request, 'core/freelancer_dashboard.html', {'proposals': proposals})