from django import forms
from django.forms.widgets import EmailInput
from .models import Profile
from django.contrib.auth.models import User


class ProfileForm(forms.Form):
    bio = forms.CharField(max_length=250, required=True)
    phone_number = forms.CharField(max_length=20)
    website = forms.URLField(max_length=100)
    picture = forms.ImageField(required=True)


class SingUpForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)
    password = forms.CharField(
        min_length=7, max_length=100, widget=forms.PasswordInput())
    password_confirm = forms.CharField(
        min_length=7, max_length=100, widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100, widget=EmailInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        query = User.objects.filter(username=username).exists()

        if query:
            raise forms.ValidationError(('Username is alredy taken!'), code='invalid')

        return username

    def clean(self):
        data = super().clean()

        password = data['password']
        password_confirm = data['password_confirm']

        if password != password_confirm:
            raise forms.ValidationError(('Passwords do not match!'), code='invalid')

    def save(self):
        data = self.cleaned_data
        data.pop('password_confirm')

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()

"""
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']


class RawUserForm(forms.Form):
    website = forms.URLField()
    bio = forms.CharField()
    phone_number = forms.CharField()
    picture = forms.ImageField()
"""
