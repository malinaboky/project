from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    firstname = forms.CharField(label="Имя", widget=forms.TextInput)
    secondname = forms.CharField(label="Фамилия", widget=forms.TextInput)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторный пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'role', 'is_staff')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = "{} {}".format(self.cleaned_data["secondname"], self.cleaned_data["firstname"])
        user.is_superuser = self.cleaned_data["is_staff"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'role', 'is_staff')
