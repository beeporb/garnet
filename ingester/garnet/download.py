"""

Module containing functionality related to downloading videos from source
websites, such as Twitch and YouTube.

"""
import pathlib

import pytube

from garnet import config


def download_video(url: str) -> pathlib.Path:
    """Downloads the video at the provided URL.

    Args:
        url (str): URL to download video from.

    Returns:
        pathlib.Path: Path to downloaded video file.
    """
    yt = pytube.YouTube(url)

    downloaded_path = yt.streams.get_highest_resolution().download(
        str(config.garnet_VIDEO_DIR)
    )

    return downloaded_path
