"""

Module containing functionality related to audio transcription.

"""
import pathlib

import whisper


def transcribe_audio_file(audio_file: str) -> dict:
    """Transcribe the provided audio file using Whisper.

    Args:
        audio_file (str): Audio file to transcribe.

    Returns:
        dict: Transcription result.
    """
    whisper_model = whisper.load_model("tiny")

    result = whisper_model.transcribe(audio_file)

    return result
