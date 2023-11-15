from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import UserSite

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class UserSiteForm(forms.ModelForm):
    class Meta:
        model = UserSite
        fields = ['name', 'url']
