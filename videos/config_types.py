from typing import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Rendition:
    label: str
    resolution: str
    bitrate: str


Renditions = Sequence[Rendition]
