import os
import dropbox
import dropbox.files
import requests

DROPBOX_LOCAL_DATA_FOLDER = os.getenv("DROPBOX_LOCAL_DATA_FOLDER")


class DropBoxManager:

    def __init__(self):
        self.app_key = os.getenv("DROPBOX_APP_KEY")
        self.app_secret = os.getenv("DROPBPOX_APP_SECRET")
        self.refresh_token = os.getenv("DROPBOX_REFRESH_TOKEN")

    def download_file(self, file: str) -> bool:
        with dropbox.Dropbox(
            oauth2_refresh_token=self.refresh_token,
            app_key=self.app_key,
            app_secret=self.app_secret,
        ) as dbx:
            response: requests.models.Response
            _, response = dbx.files_download(f"/{file}")

            local_file_path = os.path.join(DROPBOX_LOCAL_DATA_FOLDER, os.path.basename(file))

            with open(local_file_path, "wb") as f:
                f.write(response.content)

        return True

    def upload_file(self, file_name: str) -> bool:
        with dropbox.Dropbox(
            oauth2_refresh_token=self.refresh_token,
            app_key=self.app_key,
            app_secret=self.app_secret,
        ) as dbx:
            with open(f"{DROPBOX_LOCAL_DATA_FOLDER}{file_name}", "rb") as f:
                file_content = f.read()

            dbx.files_upload(
                file_content, f"/{file_name}", mode=dropbox.files.WriteMode.overwrite
            )

        return True

if __name__ == "__main__":
    # Instance of the class
    app = DropBoxManager()
    # Donwload the file
    app.download_file("tomod.txt")
    app.upload_file("tomod.txt")