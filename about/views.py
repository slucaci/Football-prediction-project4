from django.shortcuts import render
from .models import About

# Create your views here.

def about_view(request):
    """This view displays the about page."""
    about_info = About.objects.all() 
    return render(request, 'about/about.html', {'about_info': about_info})