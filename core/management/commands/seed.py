# core/management/commands/seed.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Job, Proposal
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample data.'

    def handle(self, *args, **options):
        self.stdout.write('Clearing old data...')
        Profile.objects.all().delete()
        Job.objects.all().delete()
        Proposal.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creating new data...')

        # --- Create 10 Clients ---
        client_names = ['clientA', 'clientB', 'clientC', 'clientD', 'clientE', 'clientF', 'clientG', 'clientH',
                        'clientI', 'clientJ']
        clients = []
        for name in client_names:
            user = User.objects.create_user(username=name, email=f'{name}@example.com', password='password123')
            profile = Profile.objects.create(user=user, role='client', bio=f'A new client named {name}.')
            clients.append(user)
        self.stdout.write(self.style.SUCCESS(f'Created {len(clients)} clients.'))

        # --- Create 10 Freelancers ---
        freelancer_names = ['freelancer1', 'freelancer2', 'freelancer3', 'freelancer4', 'freelancer5', 'freelancer6',
                            'freelancer7', 'freelancer8', 'freelancer9', 'freelancer10']
        freelancers = []
        for name in freelancer_names:
            user = User.objects.create_user(username=name, email=f'{name}@example.com', password='password123')
            profile = Profile.objects.create(user=user, role='freelancer', bio=f'A skilled freelancer named {name}.',
                                             hourly_rate=random.randint(20, 100))
            freelancers.append(user)
        self.stdout.write(self.style.SUCCESS(f'Created {len(freelancers)} freelancers.'))

        # --- Create 15-20 Jobs ---
        job_titles = [
            'Build a Custom Django Web App', 'Develop a Mobile-First Portfolio Site',
            'Frontend Design with React', 'Backend API for E-commerce',
            'Full-Stack Developer for SaaS Project', 'Data Analysis with Python',
            'WordPress Plugin Development', 'Database Migration Specialist',
            'Cloud Infrastructure Setup on AWS', 'UI/UX Design for a New App',
            'Write a Technical Blog Post', 'Quality Assurance Testing',
            'Machine Learning Model Training', 'Video Editing and Production',
            'Content Writer for Website'
        ]

        jobs = []
        for i, title in enumerate(job_titles):
            client = random.choice(clients)
            job = Job.objects.create(
                client=client,
                title=title,
                description=f'Looking for a professional to help with {title.lower()}. The project requires attention to detail and a strong work ethic.',
                budget=random.randint(500, 5000)
            )
            jobs.append(job)
        self.stdout.write(self.style.SUCCESS(f'Created {len(jobs)} jobs.'))

        # --- Create Proposals for each Job (1-3 proposals per job) ---
        for job in jobs:
            num_proposals = random.randint(1, 3)
            # Shuffle freelancers to get unique proposals
            random.shuffle(freelancers)

            for i in range(num_proposals):
                freelancer = freelancers[i]
                if not Proposal.objects.filter(job=job, freelancer=freelancer).exists():
                    Proposal.objects.create(
                        job=job,
                        freelancer=freelancer,
                        cover_letter=f'As a {freelancer.profile.skills} expert, I am confident I can exceed expectations on this project.',
                        rate=random.randint(int(job.budget * 0.8), int(job.budget * 1.2))
                    )
        self.stdout.write(self.style.SUCCESS('Created proposals.'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))