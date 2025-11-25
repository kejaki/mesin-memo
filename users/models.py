from django.contrib.auth.models import AbstractUser
from django.db import models

class Badge(models.Model):
    """Badges yang bisa di-assign ke user (PIC Divisi, Ketua, dll)"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Nama Badge")
    slug = models.SlugField(max_length=50, unique=True)
    color = models.CharField(max_length=20, default='blue', verbose_name="Warna", 
                            help_text="Warna badge: blue, green, red, purple, yellow, etc")
    icon = models.CharField(max_length=50, default='⭐', verbose_name="Icon/Emoji")
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    
    class Meta:
        verbose_name = "Badge"
        verbose_name_plural = "Badges"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.icon} {self.name}"

class User(AbstractUser):
    class Division(models.TextChoices):
        JOURNALISM = 'JOURNALISM', 'Jurnalistik'
        DESIGN = 'DESIGN', 'Design'
        PHOTOGRAPHY = 'PHOTOGRAPHY', 'Fotografi'
    
    class Role(models.TextChoices):
        PIC_DIVISI = 'PIC_DIVISI', 'PIC Divisi'
        KETUA = 'KETUA', 'Ketua Media Moklet'
        WAKA = 'WAKA', 'Wakil Ketua'
        SEKRETARIS = 'SEKRETARIS', 'Sekretaris'
        MEMBER = 'MEMBER', 'Anggota'

    class_name = models.CharField(max_length=50, verbose_name="Kelas/Jurusan")
    nisn = models.CharField(max_length=20, unique=True, verbose_name="NISN")
    angkatan = models.IntegerField(default=34, verbose_name="Angkatan", help_text="Contoh: 33, 34, 35")
    division = models.CharField(
        max_length=20,
        choices=Division.choices,
        default=Division.JOURNALISM,
        verbose_name="Divisi"
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
        verbose_name="Role/Jabatan"
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Nomor HP")
    is_verified = models.BooleanField(default=False, verbose_name="Terverifikasi")
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, verbose_name="Foto Profil")
    
    # Badges
    badges = models.ManyToManyField(Badge, blank=True, related_name='users', verbose_name="Badges")
    
    # Gamification
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.username} ({self.get_division_display()} - Angkatan {self.angkatan})"
    
    def has_role(self, *roles):
        """Check if user has any of the specified roles"""
        return self.role in roles or self.is_staff
    
    def can_create_content(self):
        """Only PIC Divisi can create content"""
        return self.has_role(User.Role.PIC_DIVISI) or self.is_staff
    
    def can_create_event(self):
        """PIC Divisi and Ketua can create events"""
        return self.has_role(User.Role.PIC_DIVISI, User.Role.KETUA) or self.is_staff
    
    def get_profile_photo_url(self):
        """Get profile photo URL or return None"""
        if self.profile_photo:
            return self.profile_photo.url
        return None
    
    def get_initials(self):
        """Get user initials for avatar"""
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        return self.username[0].upper()
