from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=15, required=True, help_text='Required for order updates')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    city = forms.CharField(max_length=50, required=False)
    zip_code = forms.CharField(max_length=10, required=False)
    terms = forms.BooleanField(required=True)
    newsletter = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'mobile', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Will be auto-generated from email'
        self.fields['username'].widget = forms.HiddenInput()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', mobile)
        if len(digits_only) < 10:
            raise ValidationError("Please enter a valid mobile number with at least 10 digits.")
        return mobile

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Use email as username
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user