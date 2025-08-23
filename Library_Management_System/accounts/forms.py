from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import Subscription

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

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["plan_type", "auto_renew"]

    plan_type = forms.ChoiceField(
        choices=Subscription.PLAN_CHOICES,
        widget=forms.RadioSelect,
        label="Choose a Plan"
    )

    auto_renew = forms.BooleanField(
        required=False,
        label="Enable Auto Debit (Auto Renew Monthly)"
    )