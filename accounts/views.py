from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import DetailView, UpdateView

from .forms import UserLoginForm, UserRegistrationForm
from .models import Profile, User


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


def welcome_email_register(to_email: str | None) -> bool | HttpResponse:
    if not to_email:
        return False

    try:
        send_mail(
            subject="WELCOM",
            message="We're very happy that you joined our website🌹😄😊",
            from_email=None,
            recipient_list=[to_email],
        )
    except BadHeaderError:
        return HttpResponse("Invalid header found")

    return True


def welcome_email_login(to_email: str | None) -> bool | HttpResponse:
    if not to_email:
        return False

    try:
        send_mail(
            subject="WELCOM",
            message="You are logged in on the site 🫡🌼",
            from_email=None,
            recipient_list=[to_email],
        )
    except BadHeaderError:
        return HttpResponse("Invalid header found")

    return True


def register_view(request: HttpRequest) -> HttpResponse:
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Activate your account"

            message = render_to_string(
                "authentication/email_activation/activate_email_message.html",
                {
                    "user": form.cleaned_data["username"],
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )

            to_email = form.cleaned_data["email"]
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(
                request,
                "Account created successfully.\
                Please check your email to activate your account.",
            )
            return redirect("home")
        else:
            messages.error(request, "Account creation failed. Please try again.")

    return render(request, "authentication/register.html", {"form": form})


def activate_view(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        welcome_email_register(user.email)

        return render(
            request, "authentication/email_activation/activation_successful.html"
        )

    else:
        return render(
            request, "authentication/email_activation/activation_unsuccessful.html"
        )


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            welcome_email_login(user.email)
            return redirect(
                request.POST.get("next")
                or request.GET.get("next")
                or settings.LOGIN_REDIRECT_URL
            )
        else:
            form = UserLoginForm(request)

    form = UserLoginForm(request)
    return render(request, "authentication/login.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return render(request, "authentication/logout.html")


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile"

    def get_object(self, queryset: Any = None) -> Profile:
        profile: Profile
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "accounts/profile_edit.html"
    fields = ["phone", "bio", "profile_image", "city"]
    success_url = reverse_lazy("profile_detail")

    def get_object(self, queryset: Any = None) -> Profile:
        profile: Profile
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
