from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method== 'POST':
        form= UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}!')
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
def profile(request):
    return render( request, 'users/profile.html')

@login_required
def updateProfile(request):
    if request.method== 'POST':
        update_form= UserUpdateForm(request.POST, instance=request.user)
        profile_update_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if update_form.is_valid() and profile_update_form.is_valid():
            update_form.save()
            profile_update_form.save()
            messages.success(request, f'You profile has been updated successfully!')
            return redirect('profile')
    else:
        update_form= UserUpdateForm(instance=request.user)
        profile_update_form=ProfileUpdateForm(instance=request.user.profile)
    context= {
        'update_form': update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'users/update_profile.html', context)