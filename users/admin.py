from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'angkatan', 'class_name', 'division', 'is_verified', 'points', 'is_staff')
    list_filter = ('is_verified', 'angkatan', 'division', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'nisn', 'class_name')
    actions = ['verify_users', 'unverify_users', 'add_to_member_group', 'change_division_to_journalism', 'change_division_to_design', 'change_division_to_photography']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informasi Media Moklet', {
            'fields': ('class_name', 'nisn', 'angkatan', 'division', 'phone_number', 'is_verified', 'points')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informasi Media Moklet', {
            'fields': ('class_name', 'nisn', 'angkatan', 'division', 'phone_number')
        }),
    )
    
    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f"{queryset.count()} users verified successfully.")
    verify_users.short_description = "✓ Verify selected users"
    
    def unverify_users(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, f"{queryset.count()} users unverified.")
    unverify_users.short_description = "✗ Remove verification"
    
    def add_to_member_group(self, request, queryset):
        from django.contrib.auth.models import Group
        member_group, _ = Group.objects.get_or_create(name='Member')
        for user in queryset:
            user.groups.add(member_group)
        self.message_user(request, f"{queryset.count()} users added to Member group.")
    add_to_member_group.short_description = "Add to Member group"
    
    def change_division_to_journalism(self, request, queryset):
        queryset.update(division=User.Division.JOURNALISM)
        self.message_user(request, f"{queryset.count()} users changed to Jurnalistik.")
    change_division_to_journalism.short_description = "Change division → Jurnalistik"
    
    def change_division_to_design(self, request, queryset):
        queryset.update(division=User.Division.DESIGN)
        self.message_user(request, f"{queryset.count()} users changed to Design.")
    change_division_to_design.short_description = "Change division → Design"
    
    def change_division_to_photography(self, request, queryset):
        queryset.update(division=User.Division.PHOTOGRAPHY)
        self.message_user(request, f"{queryset.count()} users changed to Fotografi.")
    change_division_to_photography.short_description = "Change division → Fotografi"
