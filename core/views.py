from django.shortcuts import render
from django.utils import timezone
from cms.models import ContentItem
from events.models import Event

def home(request):
    # Get recent content
    recent_content = ContentItem.objects.all().order_by('-created_at')[:6]
    
    # Get upcoming events
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    
    context = {
        'recent_content': recent_content,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'core/home.html', context)
