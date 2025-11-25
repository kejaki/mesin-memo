from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'coordinator', 'needs_photo', 'needs_video', 'needs_article')
    list_filter = ('date', 'needs_photo', 'needs_video', 'needs_article')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
