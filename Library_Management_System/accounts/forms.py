from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import Subscription, Comment
from datetime import date

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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "placeholder": "Write your comment or suggestion..."})
        }

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, min_length=13, required=True)
    expiry_date = forms.DateField(required=True, input_formats=["%m/%Y"])
    cvv = forms.CharField(max_length=4, min_length=3, required=True)

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not card_number.isdigit():
            raise forms.ValidationError("Card number must contain only digits.")
        if len(card_number) not in [13, 16]:
            raise forms.ValidationError("Card number must be 13 or 16 digits long.")
        return card_number

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if not cvv.isdigit():
            raise forms.ValidationError("CVV must be numeric.")
        if len(cvv) not in [3, 4]:
            raise forms.ValidationError("CVV must be 3 or 4 digits long.")
        return cvv

    def clean_expiry_date(self):
        expiry = self.cleaned_data['expiry_date']
        today = date.today()
        if expiry < date(today.year, today.month, 1):
            raise forms.ValidationError("Expiry date cannot be in the past.")
        return expiry