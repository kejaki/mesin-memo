from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Badge

# Customize admin site header
admin.site.site_header = "Media Moklet Admin"
admin.site.site_title = "Media Moklet"
admin.site.index_title = "Dashboard Admin"

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color', 'user_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    
    def user_count(self, obj):
        return obj.users.count()
    user_count.short_description = 'Jumlah User'

class BadgeInline(admin.TabularInline):
    model = User.badges.through
    extra = 1
    verbose_name = "Badge"
    verbose_name_plural = "Badges"

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'division', 'angkatan', 'is_verified', 'points']
    list_filter = ['role', 'division', 'angkatan', 'is_verified', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'nisn']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Info Anggota', {
            'fields': ('class_name', 'nisn', 'angkatan', 'division', 'role', 'phone_number', 'profile_photo')
        }),
        ('Status', {
            'fields': ('is_verified',)
        }),
        ('Gamification', {
            'fields': ('points',)
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Info Anggota', {
            'fields': ('class_name', 'nisn', 'angkatan', 'division', 'role', 'email')
        }),
    )
    
    inlines = [BadgeInline]
