from django import forms
from .models import User

class SignUpForm(forms.ModelForm):
    # Inner class is part of what's needed to construct a modelform.
    class Meta:
        # We specify the model we are referring to.
        model = User
        # ... and the list of fields we want the form to ask abt.
        fields = ["first_name","last_name","username","email","bio"]
        widgets = {"bio": forms.Textarea()}


    new_password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Password confirmation',widget=forms.PasswordInput)
