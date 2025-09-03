from django import forms
from django.contrib.auth.models import User
from .models import Job, Proposal, Profile, Message, Review


class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(
        choices=Profile.role_choices,
        widget=forms.RadioSelect,
        label="I am a:"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            role = self.cleaned_data.get('role')
            # Now, create the profile with the user's selected role
            Profile.objects.create(user=user, role=role)
        return user

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'budget', 'skills_required']


class ProposalForm(forms.ModelForm):
    # This field is now explicitly defined as not required
    attachment = forms.FileField(required=False)

    class Meta:
        model = Proposal
        fields = ['cover_letter', 'rate', 'attachment']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'hourly_rate', 'location', 'title', 'company_name']


class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Type your message here...'}))
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Message
        fields = ['body', 'file']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        }