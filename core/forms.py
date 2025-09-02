from django import forms
from django.contrib.auth.models import User
from .models import Job, Proposal, Profile


class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'budget', 'skills_required']


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['cover_letter', 'rate']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'hourly_rate', 'location', 'title', 'company_name']