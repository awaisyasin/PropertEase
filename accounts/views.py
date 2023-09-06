from django.shortcuts import render, redirect, HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
import uuid
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from accounts.models import CustomUser

# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            token = str(uuid.uuid4())
            user.email_verification_token = token
            current_site = get_current_site(request)
            verification_link = f"http://{current_site}/accounts/verify-email/{token}/"
            subject = "Email verification"
            message = f"Please follow the link below to verify your email: {verification_link}"
            from_mail = "info@propertease.com"
            recipient_list = [form.cleaned_data["email"]]
            send_mail(subject, message, from_mail, recipient_list)
            user.save()
            return redirect("accounts:login")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def verify_email_view(request, token):
    user = CustomUser.objects.get(email_verification_token=token)
    if user:
        user.is_email_verified = True
        user.email_verification_token = None
        user.save()
        return redirect("accounts:login")
    else:
        messages(request, "Invalid Email verification link!")
        return redirect("accounts:login")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_email_verified:
                login(request, user)
                return redirect("propertease:home")
            else:
                messages.error(request, "Email not verified")
                return redirect("accounts:login")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("propertease:home")