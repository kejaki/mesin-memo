from django.shortcuts import render
from django.utils import timezone
from cms.models import ContentItem
from events.models import Event
from cms.models import ContentItem
from .models import PageContent

from users.models import User

def home(request):
    # Common data
    latest_posts = ContentItem.objects.filter(status='UPLOADED').order_by('-updated_at')[:10]
    
    context = {
        'latest_posts': latest_posts,
    }

    if request.user.is_authenticated:
        # Authenticated users see upcoming events
        upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
        context['upcoming_events'] = upcoming_events
        # Guests see Top 3 Leaderboard and Members per Angkatan
        top_leaders = User.objects.filter(is_active=True).order_by('-points')[:3]
        
        # Fetch members by Angkatan
        members_33 = User.objects.filter(angkatan='33', is_active=True).order_by('?')
        members_34 = User.objects.filter(angkatan='34', is_active=True).order_by('?')
        members_35 = User.objects.filter(angkatan='35', is_active=True).order_by('?')
        
        context['top_leaders'] = top_leaders
        context['members_33'] = members_33
        context['members_34'] = members_34
        context['members_35'] = members_35
        
    return render(request, 'core/home.html', context)

def about(request):
    page = PageContent.objects.filter(key='about').first()
    if not page:
        page = PageContent(title="Tentang Kami", content="Konten belum tersedia.")
    return render(request, 'core/about.html', {'page': page})
