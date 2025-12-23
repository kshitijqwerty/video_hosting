from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from pathlib import Path

from .models import Video
from .services.transcoder import transcode
from .services.hls import generate_hls
from .services.dash import generate_dash


def upload_video(request):
    if request.method == "POST":
        title = request.POST.get("title")
        file = request.FILES.get("video")

        video = Video.objects.create(title=title, video_file=file)
        try:
            # transcode(video)
            generate_hls(video)
            generate_dash(video)
        except Exception as e:
            video.status = "failed"
            video.save()
            raise e

        return redirect("watch_video", video_id=video.id)

    return render(request, "videos/upload.html")


def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, "videos/watch.html", {"video": video})


def serve_key(request, video_id):
    key_path = Path(settings.MEDIA_ROOT) / "keys" / f"{video_id}.key"

    if not key_path.exists():
        return HttpResponse(status=404)

    return HttpResponse(key_path.read_bytes(), content_type="application/octet")
