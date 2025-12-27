import hashlib
import logging

def stream_hash(uploaded_file, chunk_size=8 * 1024 * 1024):
    hasher = hashlib.sha256()
    for chunk in uploaded_file.chunks(chunk_size):
        hasher.update(chunk)
    return hasher.hexdigest()