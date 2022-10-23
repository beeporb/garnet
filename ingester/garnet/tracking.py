"""

Module containing functionality related to tracking the progress of
transcription jobs.

"""
import enum
import uuid

import redis

gg_tracking = redis.Redis(host="redis", db=2)


class JobState(enum.Enum):
    """Tracking state for a Garnet job."""

    RECEIVED = enum.auto()
    DOWNLOADING = enum.auto()
    DOWNLOAD_FAILED = enum.auto()
    DOWNLOAD_COMPLTE = enum.auto()
    RIPPING_AUDIO = enum.auto()
    RIPPING_AUDIO_FAILED = enum.auto()
    RIPPING_AUDIO_COMPLETE = enum.auto()
    TRANSCRIBING = enum.auto()
    TRANSCRIPTION_FAILED = enum.auto()
    TRANSCRIPTION_COMPLETE = enum.auto()
    EXTRACTING_FEATURES = enum.auto()
    FEATURE_EXTRACTION_FAILED = enum.auto()
    FEATURE_EXTRACTION_COMPLETE = enum.auto()


def start_tracking_record(id: str) -> JobState:
    """Begins the tracking record for the job of provided ID.

    Args:
        id (str): ID to start tracking record for.

    Returns:
        State: Starting tracking state.
    """
    received_state = JobState.RECEIVED

    gg_tracking.hset(id, "state", received_state.value)

    return received_state


def create_job() -> str:
    """Create a new job in the tracking system.

    Returns:
        str: ID of the job.
    """
    job_id = str(uuid.uuid4())
    state = start_tracking_record(job_id)
    return job_id


def set_job_url(id: str, url: str) -> None:
    """Set the target URL of the provided job.

    Args:
        id (str): Job ID.
        url (str): Target URL.
    """
    gg_tracking.hset(id, "url", url)


def set_tracking_state(id: str, state: JobState) -> JobState:
    """Sets the tracking of the provided job to the provided state.

    Args:
        id (str): ID to change tracking record for.
        state (State): State to change the tracking record to.

    Returns:
        State: New tracking state.
    """
    gg_tracking.hset(id, "state", state.value)

    return state


def destroy_tracking_state(id: str) -> None:
    """Destroy the tracking state of the job of provided id.

    Args:
        id (str): ID of the job to destroy the tracking of.
    """

    gg_tracking.delete(id)


def wipe_tracking() -> None:
    """Wipes the tracking of ALL jobs in the tracking cache."""

    keys = gg_tracking.keys("*")

    for key in keys:
        gg_tracking.delete(key)


def dump_tracking() -> dict:
    """Dump the content of the garnet tracking cache.

    Returns:
        dict: Tracking cache dump.
    """
    keys = gg_tracking.keys("*")

    tracking_dump = {key: gg_tracking.hgetall(key) for key in keys}

    return tracking_dump
