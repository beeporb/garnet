"""

Module containing functionality related to audio extraction.

"""
import pathlib
import subprocess

from garnet import config


def extract_audio_from_video_file(video_file: pathlib.Path) -> pathlib.Path:
    """Extracts the audio from a provided video file, returning the path to it.

    Args:
        video_file (pathlib.Path): Video file to extract audio content from.

    Returns:
        pathlib.Path: Path to audio file.
    """
    audio_file = config.garnet_AUDIO_DIR / (video_file.stem + ".mp3")

    proc = subprocess.run(
        ["ffmpeg", "-i", video_file, "-q:a", "0", "-map", "a", audio_file]
    )

    return str(audio_file)
