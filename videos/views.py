from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from pathlib import Path

from .models import Video
from .tasks import process_video_async


def upload_video(request):
    if request.method == "POST":
        title = request.POST.get("title")
        file = request.FILES.get("video")

        video = Video.objects.create(title=title, video_file=file)

        process_video_async(video.id)
        
        return redirect("video_list")

    return render(request, "videos/upload.html")


def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, "videos/watch.html", {"video": video})

def video_list(request):
    videos = Video.objects.order_by("-id")
    return render(request, "videos/video_list.html", {"videos": videos})


def serve_key(request, video_id):
    key_path = Path(settings.MEDIA_ROOT) / "keys" / f"{video_id}.key"

    if not key_path.exists():
        return HttpResponse(status=404)

    return HttpResponse(key_path.read_bytes(), content_type="application/octet")
