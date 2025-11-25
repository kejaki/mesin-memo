from django.db import models

class PageContent(models.Model):
    key = models.CharField(max_length=50, unique=True, help_text="Unique key for the page (e.g., 'about')")
    title = models.CharField(max_length=200)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
