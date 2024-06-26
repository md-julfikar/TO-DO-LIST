from django import forms
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import FormActions
from bootstrap_datepicker_plus.widgets import DatePickerInput


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']
        widgets = {
            'due_date': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                }
            ),
        }


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
