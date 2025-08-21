from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# Registration form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    country = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "country", "date_of_birth")

# Login form (optional, Django has a built-in one)
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

class SubscriptionForm(forms.Form):
    PLAN_CHOICES = [
        ('FREE', 'Free'),
        ('PREMIUM', 'Premium'),
        ('UNLIMITED', 'Unlimited'),
    ]
    plan = forms.ChoiceField(choices=PLAN_CHOICES, widget=forms.RadioSelect)
