from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import ContentItem, Status, JobRoleAssignment, ActivityLog

@receiver(pre_save, sender=ContentItem)
def award_points_on_upload(sender, instance, **kwargs):
    """Award points when content status changes to UPLOADED"""
    if instance.pk:
        try:
            old_instance = ContentItem.objects.get(pk=instance.pk)
            # Check if status changed to UPLOADED
            if old_instance.status != Status.UPLOADED and instance.status == Status.UPLOADED:
                # Award points based on job roles
                role_points = {
                    'CAMERAMAN': 120,
                    'CAPTION_WRITER': 80,
                    'CONTENT_WRITER': 100,
                    'VIDEO_EDITOR': 150,
                    'THUMBNAIL_DESIGNER': 90,
                    'TALENT': 100,
                }
                
                # Get all job role assignments for this content
                assignments = JobRoleAssignment.objects.filter(
                    job_role__content=instance
                ).select_related('user', 'job_role')
                
                # Award points to each assigned user based on their role
                for assignment in assignments:
                    role_type = assignment.job_role.role_type
                    points = role_points.get(role_type, 100)
                    
                    assignment.user.points += points
                    assignment.user.save()
                    
                    # Log the point award
                    ActivityLog.objects.create(
                        user=assignment.user,
                        action=ActivityLog.Action.UPLOADED,
                        content=instance,
                        description=f"Mendapat {points} XP dari role {assignment.job_role.get_role_type_display()}"
                    )
                
                # Legacy: Award points to traditional assignments
                if instance.author and not assignments.filter(user=instance.author).exists():
                    instance.author.points += 100
                    instance.author.save()
                
                if instance.editor and not assignments.filter(user=instance.editor).exists():
                    instance.editor.points += 50
                    instance.editor.save()
                    
                if instance.designer and not assignments.filter(user=instance.designer).exists():
                    instance.designer.points += 100
                    instance.designer.save()
                    
        except ContentItem.DoesNotExist:
            pass
