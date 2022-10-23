"""

Module containing error functionality.

"""
import typing


class GarnetError(Exception):
    """Generic error for garnet."""

    def __init__(
        self, msg: typing.Optional[str] = "An error occurred."
    ) -> None:
        self.msg = msg
        super().__init__(self.msg)


class StateTrackingError(GarnetError):
    """Error reflecting issues with state tracking."""

    ...


class VideoDownloadError(GarnetError):
    """Error reflecting issues with video downloading."""

    ...


class AudioRippingError(GarnetError):
    """Error reflecting an issue when ripping the audio from the downloaded video."""

    ...


class AudioTranscriptionError(GarnetError):
    """Error reflecting an issue during audio transcription."""

    ...


class FeatureExtractionError(GarnetError):
    """Error reflecting an issue during feature extraction."""

    ...
