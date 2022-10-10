from django.shortcuts import render
from .forms import SignUpForm

# The request is an object created by Django with all info on the HTTP request received.
# Django knows to go in the templates forlder to find home.html.
def home(request):
    return render(request, 'home.html')

def sign_up(request):
    form = SignUpForm()
    return render(request, 'sign_up.html',{'form': form})
