import celery

import pathlib
import typing

from garnet.celery_config import app
from garnet import audio_extraction
from garnet import download
from garnet import tracking
from garnet import transcription


@app.task(name="transcribe_audio")
def transcribe_audio(audio_file: str, id: typing.Optional[str] = "") -> dict:
    """Entrypoint for transcribing the audio file at the provided path.

    Args:
        audio_file (str): Audio file to transcribe.
        id (typing.Optional[str], optional): Job ID that this transcription
         relates to. Defaults to "".

    Returns:
        dict: Transcription result.
    """
    state = tracking.set_tracking_state(id, tracking.JobState.TRANSCRIBING)
    result = transcription.transcribe_audio_file(audio_file)
    state = tracking.set_tracking_state(
        id, tracking.JobState.TRANSCRIPTION_COMPLETE
    )
    return result


@app.task(name="extract_audio_from_video")
def extract_audio_from_video(
    video_file: str, id: typing.Optional[str] = ""
) -> str:
    """Entrypoint for extracting audio from the video file at the provided path.

    Args:
        video_file (str): Video file to extract audio from.
        id (typing.Optional[str], optional): Job ID that this extraction relates
        to. Defaults to "".

    Returns:
        str: Path to audio file.
    """
    state = tracking.set_tracking_state(id, tracking.JobState.RIPPING_AUDIO)
    audio_file = audio_extraction.extract_audio_from_video_file(
        pathlib.Path(video_file)
    )
    state = tracking.set_tracking_state(
        id, tracking.JobState.RIPPING_AUDIO_COMPLETE
    )
    return str(audio_file)


@app.task(name="download_video_at_url")
def download_video_at_url(url: str, id: typing.Optional[str] = "") -> str:
    """Entrypoint for downloading video content from the provided URL.

    Args:
        url (str): URL to download video content from.
        id (typing.Optional[str], optional): ID of the job this download relates
        to.. Defaults to "".

    Returns:
        str: Path to downloaded video content.
    """
    state = tracking.set_tracking_state(id, tracking.JobState.DOWNLOADING)
    video_file = download.download_video(url)
    state = tracking.set_tracking_state(id, tracking.JobState.DOWNLOAD_COMPLTE)
    return str(video_file)


@app.task(name="process_url")
def process_url(url: str) -> None:
    """Entrypoint for processing a URL through Garnet.

    Args:
        url (str): URL to process.
    """
    job_id = tracking.create_job()
    state = tracking.start_tracking_record(job_id)
    tracking.set_job_url(job_id, url)
    celery.chain(
        download_video_at_url.s(url, job_id),
        extract_audio_from_video.s(job_id),
        transcribe_audio.s(job_id),
    ).apply_async()
