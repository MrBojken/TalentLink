from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    role_choices = (
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=role_choices)
    bio = models.TextField(blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    skills = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    # New field for clients
    company_name = models.CharField(max_length=100, blank=True, null=True)

def __str__(self):
        return f'{self.user.username} Profile'


class Job(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    skills_required = models.CharField(max_length=255, blank=True)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Proposal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='proposals')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals')
    cover_letter = models.TextField()
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'freelancer') # A freelancer can only submit one proposal per job

    def __str__(self):
        return f'Proposal for {self.job.title} by {self.freelancer.username}'


class Thread(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_threads')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_threads')

    class Meta:
        unique_together = ('job', 'client', 'freelancer')

    def __str__(self):
        return f'Thread for {self.job.title}'


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} on {self.timestamp.strftime("%Y-%m-%d %H:%M")}'