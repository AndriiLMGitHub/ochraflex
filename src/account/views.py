from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserSignUpForm
from .models import CustomUser
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            form = CustomUserSignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False  # Deactivate account until it is confirmed
                user.save()

                # Email confirmation
                current_site = get_current_site(request)
                subject = _("Активуйте свій акаунт")
                message = render_to_string("auth/email/account_activation_email.html", {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                })
                send_mail(subject, message, None, [
                    user.email], fail_silently=False)

                messages.success(request, _(
                    "Реєстрація успішна. Перевірте свою електронну пошту, щоб підтвердити обліковий запис."))
                return redirect("signin")
            else:
                messages.error(request, _("Please correct the errors."))
                return redirect('signup')
        else:
            form = CustomUserSignUpForm()
    return render(request, "auth/signup.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, _(
            "Ваш обліковий запис активовано. Тепер ви можете увійти."))
        return redirect("signin")
    else:
        messages.error(request, _(
            "Посилання для активації недійсне або термін його дії минув."))
        return redirect("signup")


def signin_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _(
                    "Ви успішно ввійшли."))
                return redirect('list_resumes')
            else:
                messages.error(request, _("Неправильна адреса електронної пошти або пароль."))
    return render(request, 'auth/login.html')


def signout_view(request):
    logout(request)
    messages.success(request, _("Ви успішно вийшли."))
    return redirect('signin')
