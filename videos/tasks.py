import threading
from .models import Video
from .services.hls import generate_hls
from .services.dash import generate_dash

def process_video(video_id):
    video = Video.objects.get(id=video_id)
    try:
        video.status = 'processing'
        video.save()
        generate_hls(video)
        generate_dash(video)
        video.status = 'ready'
        video.save()
    except Exception as e:
        video.status = "failed"
        video.save()
        raise e

def process_video_async(video_id):
    thread = threading.Thread(
        target=process_video,
        args=(video_id,),
        daemon=True
    )
    thread.start()