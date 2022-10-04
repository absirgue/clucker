from django.shortcuts import render

# The request is an object created by Django with all info on the HTTP request received.
# Django knows to go in the templates forlder to find home.html.
def home(request):
    return render(request, 'home.html')
