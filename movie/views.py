from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home (request):
   #return HttpResponse('<h1>welcome to Home page</h1>')
    #return render(request, 'home.html')
    return render(request, 'home.html', {'name':'Sebastian Duran Fernandez'})

def about(request):
    return HttpResponse('<h1>Welcome to About Page</h1')
    