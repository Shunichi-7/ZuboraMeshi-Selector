from django.shortcuts import render

# Create your views here.

def portfolio(request):
    return render(request, "main/portfolio.html")

def home(request):
    return render(request, "main/home.html")

