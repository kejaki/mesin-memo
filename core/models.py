from django.db import models
from .models_pages import PageContent
from .models_notifications import Notification

class ErrorLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    error_message = models.TextField()
    traceback = models.TextField()
    user = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Error Log"
        verbose_name_plural = "Error Logs"

    def __str__(self):
        return f"{self.timestamp} - {self.error_message[:50]}"
