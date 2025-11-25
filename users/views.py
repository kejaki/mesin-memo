from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserEditForm
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
    """Leaderboard with Global and individual Division tabs"""
    
    # Global leaderboard - top 50
    global_leaders = User.objects.filter(
        is_active=True
    ).select_related().prefetch_related('badges').order_by('-points')[:50]
    
    # Jurnalistik
    journalism_leaders = User.objects.filter(
        is_active=True,
        division=User.Division.JOURNALISM
    ).select_related().prefetch_related('badges').order_by('-points')[:20]
    
    # Design
    design_leaders = User.objects.filter(
        is_active=True,
        division=User.Division.DESIGN
    ).select_related().prefetch_related('badges').order_by('-points')[:20]
    
    # Photography
    photography_leaders = User.objects.filter(
        is_active=True,
        division=User.Division.PHOTOGRAPHY
    ).select_related().prefetch_related('badges').order_by('-points')[:20]
    
    # Per Angkatan
    angkatan_leaders = {}
    angkatans = User.objects.filter(is_active=True).values_list('angkatan', flat=True).distinct().order_by('-angkatan')
    for angkatan in angkatans:
        top_users = User.objects.filter(
            is_active=True,
            angkatan=angkatan
        ).select_related().prefetch_related('badges').order_by('-points')[:10]
        if top_users:
            angkatan_leaders[angkatan] = top_users
    
    context = {
        'global_leaders': global_leaders,
        'journalism_leaders': journalism_leaders,
        'design_leaders': design_leaders,
        'photography_leaders': photography_leaders,
        'angkatan_leaders': angkatan_leaders,
    }
    return render(request, 'users/leaderboard.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def members_by_angkatan(request, angkatan):
    members = User.objects.filter(angkatan=angkatan, is_active=True).order_by('-points')
    
    context = {
        'angkatan': angkatan,
        'members': members,
    }
    return render(request, 'users/members_angkatan.html', context)
