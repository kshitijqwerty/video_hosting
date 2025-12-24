from django.db import models
import uuid


class Video(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("ready", "Ready"),
        ("failed", "Failed"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)

    video_file = models.FileField(upload_to="originals/")
    hls_master = models.CharField(max_length=500)
    dash_master = models.CharField(max_length=500)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    progress = models.PositiveIntegerField(default=0)


    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
