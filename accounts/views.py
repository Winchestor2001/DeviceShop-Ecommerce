from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from .utils import send_gmail
from accounts.models import Profile, ResetPassword


def account_page(request, username):
    context = {}
    if not request.user.is_authenticated:
        return redirect('login')
    profile = Profile.objects.get(user__username=username)
    user_data = User.objects.get(profile=profile)
    if request.method == "POST":
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        if request.FILES:
            file_obj = request.FILES['photo']
            filename = f"profile/{username}_{file_obj}"
            with default_storage.open(filename, 'wb+') as d:
                for chunk in file_obj.chunks():
                    d.write(chunk)
                profile.photo = filename
            profile.save()
            return redirect('account')
        if email:
            if not email.endswith("@gmail.com"):
                email = f"{email}@gmail.com"
            profile.user.email = email
        if phone_number:
            if len(phone_number) == 13 and phone_number.startswith('+998'):
                profile.phone_number = phone_number
            else:
                context['error'] = 'Please enter phone number with +998!'
        if password:
            if len(password) >= 8:
                user_data.password = make_password(password)
            else:
                context['error'] = 'Password must be at least 8 characters!'
    profile.save()
    user_data.save()
    context['profile'] = profile

    return render(request, 'account.html', context=context)


def individual_profiles(request):
    user = User.objects.get(profile__user=request.user)
    context = {'user': user}
    return redirect(request, 'header.html', context=context)


def login_page(request):
    if not request.user.is_authenticated:
        context = {}
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            context = {
                "username": username,
                "password": password
            }
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                context['error'] = "Incorrect username or password"
        return render(request, "login.html", context=context)
    else:
        return redirect("home")


def register_page(request):
    if not request.user.is_authenticated:
        context = {}
        if request.method == "POST":
            username = request.POST.get('username')
            password1 = request.POST.get('password')
            password2 = request.POST.get('repeat_password')
            email = request.POST.get('email')
            terms = request.POST.get('terms')
            context = {
                'username': username,
                'password': password1,
                'repeat_password': password2,
                'email': email
            }
            if len(password1) >= 8:
                if not User.objects.filter(email=email).exists():
                    if not username.isdigit():
                        if not User.objects.filter(username=username).exists():
                            if password1 == password2:
                                if terms != None:
                                    user = User.objects.create_user(
                                        username=username, password=password1, email=email
                                    )
                                    Profile.objects.create(
                                        user=user
                                    )
                                    login(request, user)
                                    return redirect("home")
                                else:
                                    context['error'] = "You must confirm our terms and conditions"
                            else:
                                context['error'] = "Passwords don't match"
                        else:
                            context['error'] = "Username already taken"
                    else:
                        context['error'] = "Username mustn't contain only numbers"
                else:
                    context['error'] = "Email already taken"
            else:
                context['error'] = "Password must be at least 8 characters"
        return render(request, "register.html", context=context)
    else:
        return redirect('home')


def logout_page(request):
    logout(request)
    return redirect('login')


def forgot_password_page(request):
    context = {}
    if request.method == 'POST':
        error = send_gmail(request.POST.get('email'))
        if error:
            context['error'] = error
    return render(request, 'forgot_password.html', context=context)


def change_password_page(request, id):
    context = {}
    if request.method == 'POST':
        if ResetPassword.objects.filter(url=id).exists():
            password1 = request.POST.get('password')
            password2 = request.POST.get('repeat_password')
            if len(password1) >= 8:
                if password1 == password2:
                    user = ResetPassword.objects.get(url=id).user
                    user.set_password(password1)
                    user.save()
                    return redirect('login')
                else:
                    context['error'] = "Passwords don't match"
            else:
                context['error'] = "Password must be at least 8 characters"
    return render(request, 'change_password.html', context=context)