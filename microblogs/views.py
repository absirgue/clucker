from django.shortcuts import redirect,render
from .forms import SignUpForm
from .models import User

# The request is an object created by Django with all info on the HTTP request received.
# Django knows to go in the templates forlder to find home.html.
def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) # request.POST contains a dictionary of the data that has been posted.
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html',{'form': form})

def feed(request):
    return render(request, 'feed.html')

def log_in(request):
    return render(request, 'log_in.html')
