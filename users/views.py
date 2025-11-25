from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileEditForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request, username=None):
    if username:
        user_profile = get_object_or_404(User, username=username)
    else:
        user_profile = request.user
        
    context = {
        'profile_user': user_profile,
        'is_own_profile': request.user == user_profile
    }
    return render(request, 'users/profile.html', context)

@login_required
def leaderboard(request):
    # Get top 10 users by points
    top_users = User.objects.filter(is_active=True).order_by('-points')[:10]
    
    context = {
        'top_users': top_users,
    }
    return render(request, 'users/leaderboard.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def members_by_angkatan(request, angkatan):
    members = User.objects.filter(angkatan=angkatan, is_active=True).order_by('-points')
    
    context = {
        'angkatan': angkatan,
        'members': members,
    }
    return render(request, 'users/members_angkatan.html', context)
