from django.db import models
from django.conf import settings

class Status(models.TextChoices):
    IDEA = 'IDEA', 'Ide'
    IN_PROGRESS = 'IN_PROGRESS', 'Sedang Dikerjakan'
    REVIEW = 'REVIEW', 'Review'
    FINAL = 'FINAL', 'Final'
    UPLOADED = 'UPLOADED', 'Diupload'

class Type(models.TextChoices):
    MOTANYA = 'MOTANYA', 'Motanya'
    MELAPOR = 'MELAPOR', 'Melapor'
    PODCAST = 'PODCAST', 'Podcast'
    BEMO = 'BEMO', 'Bemo'
    BESMO = 'BESMO', 'Besmo'
    IG_STORY = 'IG_STORY', 'IG Story'

class Platform(models.TextChoices):
    INSTAGRAM = 'INSTAGRAM', 'Instagram'
    YOUTUBE = 'YOUTUBE', 'YouTube'
    TIKTOK = 'TIKTOK', 'TikTok'
    WEBSITE = 'WEBSITE', 'Website'

class RoleType(models.TextChoices):
    CAMERAMAN = 'CAMERAMAN', '📷 Cameraman'
    CAPTION_WRITER = 'CAPTION_WRITER', '✍️ Caption Writer'
    CONTENT_WRITER = 'CONTENT_WRITER', '📝 Content Writer'
    VIDEO_EDITOR = 'VIDEO_EDITOR', '🎬 Video Editor'
    THUMBNAIL_DESIGNER = 'THUMBNAIL_DESIGNER', '🖼️ Thumbnail Designer'
    TALENT = 'TALENT', '🎭 Talent'

class ContentItem(models.Model):
    title = models.CharField(max_length=200, verbose_name="Judul")
    content_type = models.CharField(max_length=50, choices=Type.choices, verbose_name="Jenis Konten")
    platform = models.CharField(max_length=50, choices=Platform.choices, verbose_name="Platform")
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.IDEA, verbose_name="Status")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    target_date = models.DateField(null=True, blank=True, verbose_name="Target Tanggal")
    
    # Assignments (Legacy - kept for backward compatibility)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authored_content',
        verbose_name="Penulis"
    )
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='edited_content',
        verbose_name="Editor"
    )
    designer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='designed_content',
        verbose_name="Desainer"
    )
    
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi")
    draft_link = models.URLField(blank=True, null=True, verbose_name="Link Draft")
    final_link = models.URLField(blank=True, null=True, verbose_name="Link Final")
    documentation_link = models.URLField(blank=True, null=True, verbose_name="Link Dokumentasi")
    
    # Job Claiming System
    is_claimable = models.BooleanField(default=False, verbose_name="Bisa Diambil?", help_text="Centang jika konten bisa diambil oleh member")
    claimed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='claimed_jobs',
        verbose_name="Diambil Oleh"
    )
    claimed_at = models.DateTimeField(null=True, blank=True, verbose_name="Waktu Diambil")

    class Meta:
        verbose_name = "Content Item"
        verbose_name_plural = "Content Items"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def get_required_roles(self):
        """Get all required job roles for this content"""
        return self.job_roles.all()
    
    def get_available_roles(self):
        """Get roles that still need people"""
        return self.job_roles.filter(assignments__isnull=True) | self.job_roles.annotate(
            assigned_count=models.Count('assignments')
        ).filter(assigned_count__lt=models.F('slots_needed'))


class JobRole(models.Model):
    """Job roles required for a content item"""
    content = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name='job_roles')
    role_type = models.CharField(max_length=50, choices=RoleType.choices, verbose_name="Jenis Role")
    slots_needed = models.PositiveIntegerField(default=1, verbose_name="Jumlah Orang Dibutuhkan")
    description = models.TextField(blank=True, verbose_name="Deskripsi Role", help_text="Optional: Jelaskan detail role ini")
    
    class Meta:
        verbose_name = "Job Role"
        verbose_name_plural = "Job Roles"
        unique_together = ['content', 'role_type']  # One role type per content
    
    def __str__(self):
        return f"{self.get_role_type_display()} for {self.content.title}"
    
    def get_assigned_count(self):
        """Count how many people have been assigned"""
        return self.assignments.count()
    
    def get_slots_remaining(self):
        """Calculate remaining slots"""
        return max(0, self.slots_needed - self.get_assigned_count())
    
    def is_full(self):
        """Check if all slots are filled"""
        return self.get_assigned_count() >= self.slots_needed


class JobRoleAssignment(models.Model):
    """Assignment of a user to a specific job role"""
    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE, related_name='assignments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Job Role Assignment"
        verbose_name_plural = "Job Role Assignments"
        unique_together = ['job_role', 'user']  # User can only take one slot per role
    
    def __str__(self):
        return f"{self.user.username} - {self.job_role.get_role_type_display()}"


class ContentComment(models.Model):
    content = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(verbose_name="Komentar")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.content.title}"


class ActivityLog(models.Model):
    class Action(models.TextChoices):
        CREATED = 'CREATED', 'Membuat Konten'
        CLAIMED = 'CLAIMED', 'Mengambil Job'
        COMPLETED = 'COMPLETED', 'Menyelesaikan Konten'
        COMMENTED = 'COMMENTED', 'Berkomentar'
        UPLOADED = 'UPLOADED', 'Upload Konten'
        CLAIMED_ROLE = 'CLAIMED_ROLE', 'Mengambil Role'
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=20, choices=Action.choices)
    content = models.ForeignKey(ContentItem, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()}"
