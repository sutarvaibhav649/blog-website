from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    return render(request,'index.html')

def blog(request):
    return render(request,'home.html')