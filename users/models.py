from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Division(models.TextChoices):
        JOURNALISM = 'JOURNALISM', 'Jurnalistik'
        DESIGN = 'DESIGN', 'Design'
        PHOTOGRAPHY = 'PHOTOGRAPHY', 'Fotografi'

    class_name = models.CharField(max_length=50, verbose_name="Kelas/Jurusan")
    nisn = models.CharField(max_length=20, unique=True, verbose_name="NISN")
    angkatan = models.IntegerField(default=34, verbose_name="Angkatan", help_text="Contoh: 33, 34, 35")
    division = models.CharField(
        max_length=20,
        choices=Division.choices,
        default=Division.JOURNALISM,
        verbose_name="Divisi"
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Nomor HP")
    is_verified = models.BooleanField(default=False, verbose_name="Terverifikasi")
    
    # Gamification
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.username} ({self.get_division_display()} - Angkatan {self.angkatan})"
