from pathlib import Path
from typing import Mapping


def download_drive_file(file_id: str, service_account_info: Mapping, destination: Path) -> None:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload

    credentials = Credentials.from_service_account_info(
        dict(service_account_info),
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
    )
    service = build("drive", "v3", credentials=credentials, cache_discovery=False)
    request = service.files().get_media(fileId=file_id)

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
