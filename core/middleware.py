from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

class VerificationMiddleware:
    """Middleware to check verification and role-based permissions"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that require PIC Divisi role
        self.pic_only_urls = [
            '/cms/create/',
        ]
        # URLs that require PIC or Ketua role
        self.pic_ketua_urls = [
            '/events/create/',
        ]
        # URLs that require general verification
        self.verified_urls = [
            '/cms/jobs/',
        ]
        # URLs that don't require any special permission
        self.excluded_urls = [
            '/admin/',
            '/accounts/login/',
            '/accounts/logout/',
            '/accounts/register/',
            '/auth/profile/edit/',
            '/auth/profile/',
            '/cms/dashboard/',
            '/cms/content/',
            '/cms/jobs/my/',
        ]

    def __call__(self, request):
        # Skip middleware for excluded URLs
        for url in self.excluded_urls:
            if request.path.startswith(url):
                return self.get_response(request)
        
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Staff members bypass all checks
            if request.user.is_staff:
                return self.get_response(request)
            
            # Check PIC-only URLs
            for url in self.pic_only_urls:
                if request.path.startswith(url):
                    if not request.user.can_create_content():
                        messages.error(
                            request,
                            '🚫 Hanya PIC Divisi yang dapat membuat konten baru. '
                            'Hubungi admin jika Anda merasa ini adalah kesalahan.'
                        )
                        return redirect('cms_dashboard')
            
            # Check PIC/Ketua URLs
            for url in self.pic_ketua_urls:
                if request.path.startswith(url):
                    if not request.user.can_create_event():
                        messages.error(
                            request,
                            '🚫 Hanya PIC Divisi dan Ketua yang dapat membuat event. '
                            'Hubungi admin jika Anda merasa ini adalah kesalahan.'
                        )
                        return redirect('event_list')
            
            # Check general verification
            if not request.user.is_verified:
                for url in self.verified_urls:
                    if request.path.startswith(url):
                        messages.warning(
                            request,
                            '⏳ Akun Anda sedang menunggu verifikasi sebagai anggota Media Moklet. '
                            'Silakan hubungi admin untuk verifikasi.'
                        )
                        return redirect('profile')
        
        response = self.get_response(request)
        return response

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        import traceback
        from .models import ErrorLog
        
        user = str(request.user) if request.user.is_authenticated else 'Anonymous'
        
        ErrorLog.objects.create(
            path=request.path,
            method=request.method,
            error_message=str(exception),
            traceback=traceback.format_exc(),
            user=user
        )
        return None
