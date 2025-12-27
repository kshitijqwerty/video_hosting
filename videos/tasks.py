import threading
from .models import Video
from .services.hls import generate_hls
from .services.dash import generate_dash

def process_video(video_id):
    video = Video.objects.get(id=video_id)
    videoAsset = video.asset
    if videoAsset.status == 'ready':
        return
    try:
        videoAsset.status = 'processing'
        videoAsset.save()
        generate_hls(videoAsset)
        generate_dash(videoAsset)
        videoAsset.status = 'ready'
        videoAsset.save()
    except Exception as e:
        videoAsset.status = "failed"
        videoAsset.save()
        raise e

def process_video_async(video_id):
    thread = threading.Thread(
        target=process_video,
        args=(video_id,),
        daemon=True
    )
    thread.start()