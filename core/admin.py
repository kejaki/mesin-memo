from django.contrib import admin
from .models import ErrorLog, PageContent

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'key', 'updated_at')

@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'path', 'method', 'error_message', 'user')
    list_filter = ('timestamp', 'method')
    search_fields = ('error_message', 'path', 'user')
    readonly_fields = ('timestamp', 'path', 'method', 'error_message', 'traceback', 'user')
    
    def has_add_permission(self, request):
        return False
