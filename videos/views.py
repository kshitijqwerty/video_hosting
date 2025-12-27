from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.db import IntegrityError, transaction

from pathlib import Path

from .models import Video, VideoAsset
from .tasks import process_video_async
from .utils import stream_hash


def upload_video(request):
    if request.method == "POST":
        title = request.POST.get("title")
        file = request.FILES.get("video")

        file.seek(0)
        file_hash = stream_hash(file)
        file.seek(0)

        try:
            with transaction.atomic():
                asset = VideoAsset.objects.create(
                    video_file=file,
                    content_hash=file_hash,
                    size=file.size,
                )
                asset_created = True
                
        except:
            asset = VideoAsset.objects.get(content_hash=file_hash)
            asset_created = False
        

        video = Video.objects.create(
            title=title,
            asset=asset,
        )
        if asset_created or asset.status != 'ready':
            process_video_async(video.id)

        return redirect("video_list")

    return render(request, "videos/upload.html")

def watch_video(request, video_id):
    video = get_object_or_404(
        Video.objects.select_related("asset"),
        id=video_id,
    )
    return render(request, "videos/watch.html", {"video": video})

def video_list(request):
    videos = Video.objects.select_related("asset").order_by("-id")
    return render(request, "videos/video_list.html", {"videos": videos})


def serve_key(request, asset_id):
    asset = get_object_or_404(
        VideoAsset,
        content_hash=asset_id,
    )

    key_path = Path(settings.MEDIA_ROOT) / "keys" / f"{asset.content_hash}.key"
    if not key_path.exists():
        return HttpResponse(status=404)

    response = HttpResponse(
        key_path.read_bytes(),
        content_type="application/octet-stream",
    )
    response["Cache-Control"] = "no-store"
    return response
