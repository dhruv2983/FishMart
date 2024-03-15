from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSignUpForm(UserCreationForm):
    is_seller = forms.BooleanField(required=False, label='Register as seller')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_seller')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = self.cleaned_data['is_seller']
        user.is_buyer = not self.cleaned_data['is_seller']
        if commit:
            user.save()
        return user
