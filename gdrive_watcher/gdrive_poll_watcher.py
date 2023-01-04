from dataclasses import dataclass, field
from datetime import datetime
import os
from typing import Iterable, List
import time
import google.auth
import google.auth.transport.requests
import google.auth.transport.urllib3
import googleapiclient.discovery
import googleapiclient.errors
from .gdrive_event import GDriveEvent, FileEventType


@dataclass
class GDrivePollWatcher:
    """
    Watch a Google Drive folder for changes.

    TODO: Add support for the user to set the time zone.
    """

    folder_id: str  # Google drive folder ID. If None, watch all folders.
    id: str = str(int(time.time() * 1000))  # ID of the watched folder.
    file_only: bool = False  # If True, only watch files, not folders.
    watch_start_time: datetime = datetime.now()
    sleep_time: int = 10  # Time (in seconds) to sleep between checks for changes
    # For authentication.
    scopes: List[str] = field(
        default_factory=lambda: ["https://www.googleapis.com/auth/drive"]
    )

    def watch(self) -> Iterable[GDriveEvent]:
        # Return newly added or modified files.

        # Ignore files modified before this time.

        service = self._authenticate()
        since = self.watch_start_time
        while True:
            recently_modified_files = list(
                self._get_recently_modified_files_recursively(
                    service, modified_since=since, folder_id=self.folder_id
                )
            )
            if self.file_only:
                recently_modified_files = [
                    file
                    for file in recently_modified_files
                    if not file["mimeType"].startswith(
                        "application/vnd.google-apps.folder"
                    )
                ]
            for file in recently_modified_files:
                yield GDriveEvent(
                    folder_id=self.folder_id,
                    file_id=file["id"],
                    file_name=file["name"],
                    relative_path=self._get_relative_path(
                        service=service,
                        parent_ids=file["parents"],
                        file_name=file["name"],
                    ),
                    event_type=FileEventType.UPDATED,
                    event_datetime=datetime.now(),
                    file_created_datetime=datetime.strptime(
                        file["createdTime"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    size=file.get("size"),
                    mime_type=file.get("mimeType"),
                )
            if recently_modified_files:
                modified_time_for_most_recent_file = datetime.strptime(
                    recently_modified_files[0]["modifiedTime"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                since = modified_time_for_most_recent_file

            time.sleep(self.sleep_time)

    def _authenticate(self):
        creds, self.project_id = google.auth.default(scopes=self.scopes)
        self.service = googleapiclient.discovery.build("drive", "v3", credentials=creds)
        return self.service

    def _get_recently_modified_files_recursively(
        self, service, folder_id: str, modified_since: datetime
    ) -> Iterable[dict]:
        children = self._get_recently_modified_files(
            service,
            modified_since=modified_since,
            folder_id=folder_id,
            files_only=False,
        )
        for child in children:
            if child["mimeType"] == "application/vnd.google-apps.folder":
                yield from self._get_recently_modified_files_recursively(
                    service, folder_id=child["id"], modified_since=modified_since
                )
            else:
                yield child

    def _get_recently_modified_files(
        self, service, folder_id: str, modified_since: datetime, files_only=True
    ) -> List[dict]:
        """
        Example output:

        [
            {'size': '1024', 'id': '1LI8dE1zWjIAkHV2Qoekyz7HMhzli57Ir6sIi9OG8fks', 'name': 'test0', 'createdTime': '2022-12-27T04:21:43.801Z', 'modifiedTime': '2022-12-27T04:21:47.614Z'},
        ]
        """
        files = []
        try:
            page_token = None
            while True:
                response = (
                    service.files()
                    .list(
                        q=f"'{folder_id}' in parents",
                        spaces="drive",
                        fields="nextPageToken, "
                        "files(id, modifiedTime, name, size, parents, createdTime, mimeType)",
                        orderBy="modifiedTime desc",
                        pageToken=page_token,
                    )
                    .execute()
                )
                # print(response)
                reached_start_time = False
                for file in response.get("files", []):
                    # Save the file ID and modified time
                    modified_time = datetime.strptime(
                        file["modifiedTime"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                    if modified_time > modified_since:
                        if files_only:
                            if file["mimeType"] != "application/vnd.google-apps.folder":
                                assert "parents" in file, str(file)
                                files.append(file)
                        else:
                            files.append(file)
                    else:
                        reached_start_time = True
                        break
                if reached_start_time:
                    break
                page_token = response.get("nextPageToken", None)
                if page_token is None:
                    print(f"Found {len(files)} files in the folder")
                    break
                if len(files) == 0:
                    print("No files found.")
                    break

        except googleapiclient.errors.HttpError as error:
            print(f"An error occurred: {error}")
            raise
        return files

    def _get_relative_path(
        self, service, parent_ids: List[str], file_name: str
    ) -> List[str]:
        """
        Get the relative path of a file or folder.
        :param parent_ids: The IDs of the parent folders.
        :return: The relative path of the file or folder.
        """
        relative_path = []
        for parent_id in parent_ids:
            if parent_id == self.folder_id:
                continue
            parent = service.files().get(fileId=parent_id, fields="name").execute()
            relative_path.append(parent["name"])
        relative_path = relative_path + [file_name]
        relative_path = os.path.join(*relative_path)
        return relative_path
