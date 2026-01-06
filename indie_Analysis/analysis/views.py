from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def home(request):
    return HttpResponse("Indie Game Analysis Dashboard")

def login_required_page(request):
    return HttpResponse("Please log in to view the data analysis")

def contact(request):
    return HttpResponse("Contact Us Page")

# Protected Analysis Page
@login_required(login_url = "/login-required/")
def q1(request):
    return HttpResponse("Q1-Genre analysis place holder")

@login_required(login_url = "/login-required/")
def q2(request):
    return HttpResponse("Q2- Price Analysis (placeholder)")

@login_required(login_url="/login-required")
def q3(request):
    return HttpResponse("Q3 - Language and Engagement Analysis Placeholder")

#Registration 
def register(request):
    if request.method == "POST":
        full_name = request.POST.get("name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username = username).exists():
            messages.error(request)
            return redirect("register")
        user = User.objects.create_user(
            username=username,
            password=password
        )


        user.first_name = full_name
        user.save()

        login(request,user)
        return redirect("home")


     

    return render(request, "register.html")

