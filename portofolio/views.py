# creating a 'view' that returns an HTML template
# this function will return file : index.html, when called

from django.shortcuts import render

def landing_page(request):
    return render(request, "index.html")