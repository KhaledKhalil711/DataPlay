from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from statistical_analysis.q2_analysis import create_histogram,create_price_buckets,get_statistics


# Create your views here.
def home(request):
    return render(request, "index.html")

def login_required_page(request):
    return render(request, "login_required.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
          # Find user by email
        # try:
        user_obj = User.objects.get(email=email)
        user = authenticate(request, username=user_obj.email, password=password)
            
        if user is not None:
                auth_login(request, user)
                # Redirect to the page they were trying to access, or home
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
                messages.error(request, "Email ou mot de passe incorrect")
        # except User.DoesNotExist:
        #     messages.error(request, "Email ou mot de passe incorrect")
    
    return render(request, "connecter.html")

# Protected Analysis Page
@login_required(login_url = "/login-required/")
def q1(request):
    return render(request, "q1.html")

@login_required(login_url="/login-required/")
def q2(request):
    """Q2 - Price Analysis"""
    context = {
        'chart1': create_histogram(),
        'chart2': create_price_buckets(),
        'stats': get_statistics()
    }
    return render(request, 'q2.html', context)

@login_required(login_url="/login-required")
def q3(request):
    return render(request, "q3.html")

#Registration 
def register(request):
    if request.method == "POST":
        full_name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "email a déjà utilisé")
            return redirect("register")

        user = User.objects.create_user(
            username = email,
            email=email,
            password=password
        )
        user.first_name = full_name
        user.save()

        auth_login(request, user)
        return redirect("home")

    return render(request, "inscription.html")

