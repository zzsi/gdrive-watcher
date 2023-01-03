from dataclasses import dataclass
import io
from typing import List
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from .gdrive_authenticator import GDriveAuthenticator


@dataclass
class GDriveWriter:
    output_folder_id: str

    def __post_init__(self):
        self.authenticator = GDriveAuthenticator()

    def write(self, relative_path: str, content: bytes) -> str:
        """
        Write the content to a file using Google Drive API.

        Args:
            relative_path: The relative path of the file to write. For example,
                if the output folder is "a", and the relative path is "b/c/d.txt",
                then this function will create a directory "b" in "a", and then
                create a directory "c" in "b", and then create a file "d.txt" in
                "c".
            content: The binary content to write to the file.
        Returns:
            The file ID of the file that was written.

        """
        service = self.authenticator.authenticate()
        parts = relative_path.split("/")
        dirs = parts[:-1]
        filename = parts[-1]
        parent_folder_id = self.makedirs(dirs)
        existing = self.find_files(parent_folder_id, filename)
        f = io.BytesIO(content)
        media = MediaIoBaseUpload(f, mimetype="application/octet-stream")
        if existing:
            print(f"File {relative_path} already exists. Overwriting...")
            existing_id = existing[0]["id"]
            file = (
                service.files().update(fileId=existing_id, media_body=media).execute()
            )
            return file["id"]
        else:
            file_metadata = {"name": filename, "parents": [parent_folder_id]}
            file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            return file["id"]

    def makedirs(self, dirs: List[str]) -> str:
        """
        Create a nested subdirectory in the output folder. `dirs` represents
        one nested subdirectory. For example, if `dirs` is ["a", "b", "c"],
        then this function will create a directory "a" in the output folder,
        and then create a directory "b" in "a", and then create a directory
        "c" in "b". The function returns the ID of the last directory created.
        """
        service = self.authenticator.authenticate()
        parent_folder_id = self.output_folder_id
        for dir in dirs:
            existing = self.find_dirs(parent_folder_id, dir)
            if not existing:
                parent_folder_id = self._create_folder(service, parent_folder_id, dir)
            else:
                parent_folder_id = existing[0]["id"]
        return parent_folder_id

    def find_dirs(self, parent_folder_id: str, name: str) -> bool:
        """
        Check if a folder exists in the parent folder. Returns a list of
        folders with the same name in the parent folder.
        """
        service = self.authenticator.authenticate()
        response = (
            service.files()
            .list(
                q=f"'{parent_folder_id}' in parents and name='{name}' and mimeType='application/vnd.google-apps.folder'",
                spaces="drive",
                fields="files(id, name)",
            )
            .execute()
        )
        files = response.get("files", [])
        return files

    def find_files(self, parent_folder_id: str, name: str) -> bool:
        """
        Check if a file exists in the parent folder. Returns a list of
        files with the same name in the parent folder.
        """
        service = self.authenticator.authenticate()
        response = (
            service.files()
            .list(
                q=f"'{parent_folder_id}' in parents and name='{name}' and mimeType!='application/vnd.google-apps.folder'",
                spaces="drive",
                fields="files(id, name)",
            )
            .execute()
        )
        files = response.get("files", [])
        return files

    def _create_folder(self, service, parent_folder_id: str, folder_name: str) -> str:
        """
        Create a folder in the parent folder.

        Args:
            service: The Google Drive API service.
            parent_folder_id: The ID of the parent folder.
            folder_name: The name of the folder to create.
        Returns:
            The ID of the folder created.
        """
        file_metadata = {
            "name": folder_name,
            "parents": [parent_folder_id],
            "mimeType": "application/vnd.google-apps.folder",
        }
        file = service.files().create(body=file_metadata, fields="id").execute()
        return file.get("id")


if __name__ == "__main__":
    """
    python -m gdrive_watcher.gdrive_writer
    """
    from dotenv import load_dotenv
    import os

    load_dotenv()
    writer = GDriveWriter(output_folder_id=os.environ["OUTPUT_FOLDER_ID"])
    writer.write(relative_path="folder0/test.txt", content=b"test output 2")
