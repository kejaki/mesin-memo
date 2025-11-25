from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nama Event")
    date = models.DateTimeField(verbose_name="Tanggal & Waktu")
    description = models.TextField(verbose_name="Deskripsi Singkat")
    location = models.CharField(max_length=200, verbose_name="Lokasi")
    
    # Coverage Needs
    needs_photo = models.BooleanField(default=False, verbose_name="Butuh Foto")
    needs_video = models.BooleanField(default=False, verbose_name="Butuh Video")
    needs_article = models.BooleanField(default=False, verbose_name="Butuh Artikel")
    
    coordinator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='coordinated_events', verbose_name="Koordinator (PIC)")
    
    # Documentation Links
    documentation_link = models.URLField(blank=True, verbose_name="Link Dokumentasi")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
