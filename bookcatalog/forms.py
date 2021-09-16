from django import forms
from django.contrib.auth.models import User
from django.db.models import fields
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comments',)


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')