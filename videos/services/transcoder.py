import subprocess
from pathlib import Path
from django.conf import settings
from django.core.files import File
from ..config import VIDEO_RENDITIONS


def transcode(video):
    input_path = video.video_file.path

    for _, r in enumerate(VIDEO_RENDITIONS):

        label = r.label
        resolution = r.resolution

        output_dir = Path(settings.MEDIA_ROOT) / "processed" / f"{label}"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filename = f"{video.id}_{label}.mp4"

        output_path = output_dir / f"{video.id}_{label}.mp4"

        command = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-vf",
            f"scale={resolution}",
            "-c:a",
            "copy",
            str(output_path),
        ]
        subprocess.run(command, check=True)

        with open(output_path, "rb") as f:
            django_file = File(f)
            getattr(video, f"processed_{label}").save(
                output_filename, django_file, save=False
            )

    video.status = "ready"
    video.save()
