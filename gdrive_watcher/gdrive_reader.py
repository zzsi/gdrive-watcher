from .gdrive_authenticator import GDriveAuthenticator


class GDriveReader:
    def __init__(self):
        self.authenticator = GDriveAuthenticator()

    def read_by_file_id(self, file_id: str) -> bytes:
        """
        Read the contents of a file using Google Drive API.
        """
        service = self.authenticator.authenticate()
        request = service.files().get_media(fileId=file_id)
        binary_content = request.execute()
        return binary_content
