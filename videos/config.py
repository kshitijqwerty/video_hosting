from videos.config_types import Rendition, Renditions

DASH_RENDITIONS: Renditions = [
    Rendition("144p", "256x144", "150k"),
    Rendition("360p", "640x360", "800k"),
    Rendition("480p", "854x480", "1400k"),
    Rendition("720p", "1280x720", "2800k"),
]

HLS_RENDITIONS: Renditions = [
    Rendition("144p", "256x144", "150k"),
    Rendition("360p", "640x360", "800k"),
    Rendition("480p", "854x480", "1400k"),
    Rendition("720p", "1280x720", "2800k"),
]

VIDEO_RENDITIONS: Renditions = [
    Rendition("144p", "256x144", "150k"),
    Rendition("360p", "640x360", "800k"),
    Rendition("480p", "854x480", "1400k"),
    Rendition("720p", "1280x720", "2800k"),
]