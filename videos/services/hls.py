import subprocess
from pathlib import Path
from django.conf import settings
from .keys import generate_key

from ..config import HLS_RENDITIONS


def generate_hls(video):
    input_path = video.video_file.path

    video_asset_id = str(video.content_hash)

    hls_dir = Path(settings.MEDIA_ROOT) / "hls" / video_asset_id
    hls_dir.mkdir(parents=True, exist_ok=True)

    master_playlist = hls_dir / "master.m3u8"

    variant_entries = []
    # Key management

    key_path = generate_key(video_asset_id)

    keyinfo = hls_dir / "keyinfo.txt"
    keyinfo.write_text(f"http://127.0.0.1:8000/keys/{video_asset_id}/\n" f"{key_path}\n")

    # 🔍 HARD ASSERT (IMPORTANT)
    if keyinfo.stat().st_size == 0:
        raise RuntimeError("keyinfo.txt is empty")

    for i, r in enumerate(HLS_RENDITIONS):
        playlist = hls_dir / f"{r.label}.m3u8"

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-vf",
            f"scale={r.resolution}",
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
            r.bitrate,
            "-maxrate",
            r.bitrate,
            "-bufsize",
            "2M",
            "-hls_key_info_file",
            str(keyinfo),
            "-hls_segment_filename",
            str(hls_dir / f"{r.label}_%03d.ts"),
            str(playlist),
        ]

        subprocess.run(cmd, check=True)

        variant_entries.append(
            f"#EXT-X-STREAM-INF:BANDWIDTH={r.bitrate.replace('k','000')},RESOLUTION={r.resolution}\n{r.label}.m3u8"
        )

    master_playlist.write_text("#EXTM3U\n" + "\n".join(variant_entries))

    video.hls_master = f"hls/{video_asset_id}/master.m3u8"
    video.save(update_fields=["hls_master"])
