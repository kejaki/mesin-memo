from django.contrib import admin
from .models import ContentItem, ContentComment, ActivityLog, JobRole, JobRoleAssignment

class JobRoleInline(admin.TabularInline):
    model = JobRole
    extra = 1
    fields = ['role_type', 'slots_needed', 'description']

class JobRoleAssignmentInline(admin.TabularInline):
    model = JobRoleAssignment
    extra = 0
    readonly_fields = ['assigned_at']

@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'platform', 'status', 'target_date', 'author', 'is_claimable', 'claimed_by')
    list_filter = ('status', 'platform', 'content_type', 'is_claimable')
    search_fields = ('title', 'description')
    inlines = [JobRoleInline]
    fieldsets = (
        ('Informasi Konten', {
            'fields': ('title', 'content_type', 'platform', 'description', 'target_date')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'author', 'editor', 'designer')
        }),
        ('Job Claiming', {
            'fields': ('is_claimable', 'claimed_by', 'claimed_at')
        }),
        ('Links', {
            'fields': ('draft_link', 'final_link', 'documentation_link')
        }),
    )
    readonly_fields = ('claimed_at',)

@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ('content', 'role_type', 'slots_needed', 'get_assigned_count', 'get_slots_remaining')
    list_filter = ('role_type',)
    search_fields = ('content__title',)
    inlines = [JobRoleAssignmentInline]
    
    def get_assigned_count(self, obj):
        return obj.get_assigned_count()
    get_assigned_count.short_description = 'Assigned'
    
    def get_slots_remaining(self, obj):
        return obj.get_slots_remaining()
    get_slots_remaining.short_description = 'Remaining'

@admin.register(JobRoleAssignment)
class JobRoleAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_role', 'assigned_at')
    list_filter = ('job_role__role_type', 'assigned_at')
    search_fields = ('user__username', 'job_role__content__title')
    readonly_fields = ('assigned_at',)

@admin.register(ContentComment)
class ContentCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('message', 'user__username', 'content__title')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'description', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'description')
    readonly_fields = ('timestamp',)
