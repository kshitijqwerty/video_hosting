from django.db import models
import uuid

# Store Actual Videos
class VideoAsset(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("ready", "Ready"),
        ("failed", "Failed"),
    ]
    video_file = models.FileField(upload_to="originals/")
    size = models.BigIntegerField()
    hls_master = models.CharField(max_length=500)
    dash_master = models.CharField(max_length=500)

    content_hash = models.CharField(max_length=64, unique=True, db_index=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    progress = models.PositiveIntegerField(default=0)


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content_hash
class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)

    asset = models.ForeignKey(
        VideoAsset,
        on_delete=models.PROTECT,
        related_name="videos"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
