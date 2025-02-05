from django.shortcuts import render, redirect
from django.contrib import messages
from allauth.account.views import SignupView
from django.contrib.auth import login, logout, authenticate


# Create your views here.

def home_view(request):
    if request.user.is_authenticated:
        messages.success(request, f"Welcome back, {request.user.username}! 🎉")
    return render(request, "home/home.html")

def home_viewold(request):
    return render(request, "home/home.html")

class CustomSignupView(SignupView):
    def form_valid(self, form):
        messages.success(self.request, "Account created successfully! You can now log in.")
        return super().form_valid(form)
    
def custom_login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "account/login.html")

def custom_logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")