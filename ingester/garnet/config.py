"""

Module containing configuration functionality.

"""
import os
import pathlib

garnet_VIDEO_DIR = pathlib.Path(
    os.getenv("garnet_VIDEO_DIR", "/mnt/gg/videos")
)

garnet_AUDIO_DIR = pathlib.Path(
    os.getenv("garnet_AUDIO_DIR", "/mnt/gg/audio")
)
