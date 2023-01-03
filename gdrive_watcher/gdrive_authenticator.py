from dataclasses import dataclass, field
from typing import List
import google.auth
import google.auth.transport.requests
import googleapiclient.discovery


@dataclass
class GDriveAuthenticator:
    scopes: List[str] = field(
        default_factory=lambda: ["https://www.googleapis.com/auth/drive"]
    )

    def authenticate(self):
        if not hasattr(self, "service"):
            return self._authenticate()
        return self.service

    def _authenticate(self):
        creds, self.project_id = google.auth.default(scopes=self.scopes)
        self.service = googleapiclient.discovery.build("drive", "v3", credentials=creds)
        return self.service
