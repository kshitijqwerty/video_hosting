import subprocess
from pathlib import Path
from django.conf import settings
from django.core.files import File
from .keys import generate_key

HLS_RENDITIONS = [
    ("360p", "640x360", "800k"),
    ("480p", "854x480", "1400k"),
    ("720p", "1280x720", "2800k"),
]


def generate_hls(video):
    input_path = video.video_file.path

    hls_dir = Path(settings.MEDIA_ROOT) / "hls" / str(video.id)
    hls_dir.mkdir(parents=True, exist_ok=True)

    master_playlist = hls_dir / "master.m3u8"

    variant_entries = []
    # Key management

    key_path = generate_key(video.id)

    keyinfo = hls_dir / "keyinfo.txt"
    keyinfo.write_text(f"http://127.0.0.1:8000/keys/{video.id}/\n" f"{key_path}\n")

    # 🔍 HARD ASSERT (IMPORTANT)
    if keyinfo.stat().st_size == 0:
        raise RuntimeError("keyinfo.txt is empty")

    for label, resolution, bitrate in HLS_RENDITIONS:
        playlist = hls_dir / f"{label}.m3u8"

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-vf",
            f"scale={resolution}",
            "-c:a",
            "aac",
            "-ar",
            "48000",
            "-b:a",
            "128k",
            "-c:v",
            "h264",
            "-profile:v",
            "main",
            "-crf",
            "20",
            "-sc_threshold",
            "0",
            "-g",
            "48",
            "-keyint_min",
            "48",
            "-hls_time",
            "6",
            "-hls_playlist_type",
            "vod",
            "-b:v",
            bitrate,
            "-maxrate",
            bitrate,
            "-bufsize",
            "2M",
            "-hls_key_info_file",
            str(keyinfo),
            "-hls_segment_filename",
            str(hls_dir / f"{label}_%03d.ts"),
            str(playlist),
        ]

        subprocess.run(cmd, check=True)

        variant_entries.append(
            f"#EXT-X-STREAM-INF:BANDWIDTH={bitrate.replace('k','000')},RESOLUTION={resolution}\n{label}.m3u8"
        )

    master_playlist.write_text("#EXTM3U\n" + "\n".join(variant_entries))

    # with open(master_playlist, "rb") as f:
    #     video.hls_master.save(f"{video.id}/master.m3u8", File(f), save=True)

    video.hls_master = f"hls/{video.id}/master.m3u8"
    video.save(update_fields=["hls_master"])

    # with open(master_playlist, "rb") as f:
    #     print(f.name)
    #     getattr(video, "hls_master").save(
    #         f"{video.id}/master.m3u8", File(f), save=False
    #     )
    # video.status = 'ready'
    # video.save()
