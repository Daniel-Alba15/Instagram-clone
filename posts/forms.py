from django import forms
from .models import Post


class DeleteForm(forms.Form):
    aceptar = forms.NullBooleanField()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'user', 'profile', 'title', 'photo'}
