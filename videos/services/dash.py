import subprocess
from pathlib import Path

from django.conf import settings
from django.core.files import File

DASH_RENDITIONS = [
    {"label": "360p", "resolution": "640x360", "bitrate": "800k"},
    {"label": "480p", "resolution": "854x480", "bitrate": "1400k"},
    {"label": "720p", "resolution": "1280x720", "bitrate": "2800k"},
]

def generate_dash(video):
    input_path = video.video_file.path

    dash_dir = Path(settings.MEDIA_ROOT) / "dash" / str(video.id)
    dash_dir.mkdir(parents=True, exist_ok=True)

    mpd_path = dash_dir / "manifest.mpd"

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        
    ]

    # Map video streams dynamically
    for i, r in enumerate(DASH_RENDITIONS):
        cmd += [
            "-map", "0:v",
            f"-s:v:{i}", r["resolution"],
            f"-b:v:{i}", r["bitrate"],
        ]

    # Map audio once
    cmd += [
        "-map", "0:a?",
        "-c:a", "aac",
        "-b:a", "128k",

        "-c:v", "libx264",
        "-profile:v", "main",
        "-crf", "20",

        # DASH settings
        "-use_timeline", "1",
        "-use_template", "1",
        "-adaptation_sets", "id=0,streams=v id=1,streams=a",

        # Segment naming
        "-init_seg_name", "init-$RepresentationID$.m4s",
        "-media_seg_name", "chunk-$RepresentationID$-$Number%05d$.m4s",

        "-f", "dash",
        str(mpd_path),
    ]

    print("FFmpeg DASH:", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=dash_dir)
    for f in dash_dir.glob("manifest_*.mpd"):
        if f.name != "manifest.mpd":
            f.unlink()

    # with open(mpd_path, "rb") as f:
    #     video.dash_master.save(
    #         f"{video.id}/manifest.mpd",
    #         File(f),
    #         save=True
    #     )
    # with open(mpd_path, "rb") as f:
    #     getattr(video, "dash_master").save(
    #         f"{video.id}/manifest.mpd", File(f), save=False
    #     )

    video.dash_master = f"dash/{video.id}/manifest.mpd"
    video.save(update_fields=["dash_master"])
