# Video Streaming Platform (Django + FFmpeg) (WIP)

A video streaming platform built with **Django** and **FFmpeg** that supports
**HLS** and **MPEG-DASH** adaptive streaming.  
The project focuses on practical backend, video processing, and containerization
concepts.

---

## Features

- Video upload via Django
- Server-side video transcoding using FFmpeg
- HLS streaming with AES-128 encryption
- MPEG-DASH adaptive bitrate streaming
- Multiple video resolutions
- Playback using `hls.js` and `dash.js`
- Dockerized development environment

---

## Tech Stack

- **Backend**: Django
- **Video Processing**: FFmpeg
- **Streaming Formats**: HLS, MPEG-DASH
- **Players**: hls.js, dash.js
- **Containerization**: Docker, Docker Compose

---

## Project Structure
    ytclone/
    ├── Dockerfile
    ├── docker-compose.yml
    ├── entrypoint.sh
    ├── requirements.txt
    ├── manage.py
    ├── ytclone/
    │ └── settings.py
    ├── videos/
    │ ├── models.py
    │ ├── views.py
    │ └── ffmpeg.py
    ├── media/
    │ ├── hls/
    │ └── dash/
    └── README.md

---

## High-Level Architecture
    User
    │
    │ Upload Video
    ▼
    Django Backend
    │
    │ Save file to disk
    │
    │ Call FFmpeg
    ▼
    FFmpeg Transcoder
    │
    ├── HLS (m3u8 + ts)
    └── DASH (mpd + m4s)
    │
    ▼
    Media Storage
    │
    ▼
    Browser Player (hls.js / dash.js)

---

## Video Processing Flow
    User uploads a video

    Django saves the original file

    FFmpeg generates:

        - Multiple resolutions

        - HLS playlists and segments

        - DASH manifests and segments

    Manifest paths are stored in the database

    Client plays the video using adaptive streaming

---

## Streaming & Playback

- **DASH** is preferred when available
- **HLS** is used as a fallback
- Adaptive bitrate selection is handled by the player

---

## HLS Encryption

- AES-128 encryption enabled via FFmpeg
- Encryption keys generated per video
- Keys are referenced in the HLS playlist
- Keys are served securely by the backend

---

## Docker Setup

### Build the image
```bash
docker-compose build
```
### Run the application
```bash
docker-compose up
```
### Application runs at:
```
http://localhost:8000/upload
```