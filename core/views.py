from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UserSignUpForm, JobForm, ProposalForm, ProfileUpdateForm, MessageForm
from .models import Profile, Job, Proposal, Thread, Message


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, client=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('dashboard')

    return render(request, 'core/job_delete_confirm.html', {'job': job})


@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk, client=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully.')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)

    return render(request, 'core/job_edit.html', {'form': form, 'job': job})


@login_required
def client_dashboard(request):
    posted_jobs = request.user.posted_jobs.all()
    return render(request, 'core/client_dashboard.html', {'posted_jobs': posted_jobs})


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


# New helper function to check if the user is the thread participant
def is_thread_participant(user, thread):
    return user == thread.client or user == thread.freelancer


@login_required
@user_passes_test(is_client)
def accept_proposal(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk)
    # Only the job owner can accept a proposal
    if request.user != proposal.job.client:
        return redirect('job_detail', pk=proposal.job.pk)

    # Mark the proposal as accepted
    proposal.status = 'accepted'
    proposal.save()

    # Close the job and reject all other pending proposals
    proposal.job.is_open = False
    proposal.job.save()
    Proposal.objects.filter(job=proposal.job, status='pending').update(status='rejected')

    # Create a new message thread
    thread, created = Thread.objects.get_or_create(
        job=proposal.job,
        client=proposal.job.client,
        freelancer=proposal.freelancer
    )

    return redirect('thread_detail', pk=thread.pk)


@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    messages = thread.messages.all()

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender = request.user
            message.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = MessageForm()

    return render(request, 'core/thread_detail.html', {'thread': thread, 'messages': messages, 'form': form})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = user.profile

    context = {
        'user_profile': user_profile,
    }

    if user_profile.role == 'client':
        context['posted_jobs'] = user.posted_jobs.all()

    return render(request, 'core/profile_view.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'core/profile_edit.html', {'form': form})


def search(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('search_type', 'talent')

    results = []
    if query:
        if search_type == 'talent':
            results = Profile.objects.filter(
                role='freelancer',
                user__is_active=True
            ).filter(
                Q(skills__icontains=query) |
                Q(bio__icontains=query) |
                Q(title__icontains=query) |
                Q(user__username__icontains=query)
            ).distinct()
        elif search_type == 'jobs':
            results = Job.objects.select_related('client').filter(
                is_open=True
            ).filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(skills_required__icontains=query)
            ).distinct()

    context = {
        'query': query,
        'search_type': search_type,
        'results': results,
    }
    return render(request, 'core/search_results.html', context)