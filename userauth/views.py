from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings


from .forms import UserRegisterForm, ProfileForm
from .models import User, Profile

# User = settings.AUTH_USER_MODEL


def register_view(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hey {username}, your account was created successfully')
            
            # login automatically
            new_user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('main:index')
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }
    return render(request, 'userauth/sign-up.html', context)


def login_view(request):
    # check if user is already logged in
    if request.user.is_authenticated:
        messages.warning(request, 'Hey! You are already logged in')
        return redirect('main:index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in')
                return redirect('main:index')
            else:
                messages.warning(request, 'User Does Not Exist. Create an Account')
        except:
            messages.warning(request, f'User with {email} does not exist')

    return render(request, 'userauth/sign-in.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You are logged out!')
    return redirect('userauth:sign-in')


def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile Updated Successfully!")
            return redirect("main:dashboard")
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, "userauth/profile-update.html", context)

