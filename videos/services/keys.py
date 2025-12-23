import os
from pathlib import Path
from django.conf import settings


def generate_key(video_id):
    key_dir = Path(settings.MEDIA_ROOT) / "keys"

    key_dir.mkdir(parents=True, exist_ok=True)

    key_path = key_dir / f"{video_id}.key"

    if not key_path.exists():
        key = os.urandom(16)
        key_path.write_bytes(key)

    return key_path
