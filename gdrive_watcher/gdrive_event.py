from dataclasses import dataclass
from datetime import datetime
import enum
from typing import List


class FileEventType(enum.Enum):
    """
    The type of event that occurred to a file.
    """

    CREATED = "created"
    UPDATED = "updated"


@dataclass
class GDriveEvent:
    """An event that occurred in the watched folder."""

    folder_id: str
    file_id: str
    file_name: str
    relative_path: str  # Path relative to the watched folder
    event_type: FileEventType
    event_datetime: datetime = datetime.now()
    file_created_datetime: datetime = None
    size: int = None
    mime_type: str = None

    @property
    def is_folder(self):
        return self.mime_type == "application/vnd.google-apps.folder"
