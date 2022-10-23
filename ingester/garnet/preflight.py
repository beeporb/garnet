"""

Module containing preflight checks and tasks to be completed.

"""
import enum
import typing

import whisper

from garnet import config


def create_working_dirs() -> None:
    """Creates all working directories for garnet, as defined by envars
    or in garnet.config.
    """
    if not config.garnet_AUDIO_DIR.exists():
        config.garnet_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    if not config.garnet_VIDEO_DIR.exists():
        config.garnet_VIDEO_DIR.mkdir(parents=True, exist_ok=True)


def load_model() -> None:
    """Loads the whisper model, and then releases it. Ensures that the model has
    been downloaded on this worker.
    """
    whisper_model = whisper.load_model("tiny")
