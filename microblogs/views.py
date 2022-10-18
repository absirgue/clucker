from django.shortcuts import redirect,render
from django.contrib.auth import authenticate, login
from .forms import LogInForm, SignUpForm
from .models import User
from django.contrib import messages

# The request is an object created by Django with all info on the HTTP request received.
# Django knows to go in the templates forlder to find home.html.
def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) # request.POST contains a dictionary of the data that has been posted.
        if form.is_valid():
            # save method returns the user object is has saved
            user = form.save()
            login(request,user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html',{'form': form})

def feed(request):
    return render(request, 'feed.html')

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # authenticate checks for usern with given username, if there is one it hashes the pwd and checks if it's the same as the one in the DB.
            user = authenticate(username=username, password= password)
            if user is not None:
                # Logging in the user effectively means creating the _auth_user_id variable in the client's session
                login(request, user)
                return redirect('feed')
        # Add error message here bcs it corresponds to an incorrect LogIn
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})
