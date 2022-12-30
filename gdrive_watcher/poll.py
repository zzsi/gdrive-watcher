import os
import google.auth
import google.auth.transport.requests
import google.auth.transport.urllib3
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Set up the Drive API client
SCOPES = ["https://www.googleapis.com/auth/drive"]
creds, project_id = google.auth.default(scopes=SCOPES)
print(f"Project ID: {project_id}")
service = googleapiclient.discovery.build("drive", "v3", credentials=creds)

# Set the ID of the folder you want to watch
folder_id = os.environ["FOLDER_ID"]

# List the files in the folder and save their metadata
def get_folder_contents():
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
                    "files(id, modifiedTime, name, parents, size, createdTime)",
                    orderBy="modifiedTime desc",
                    pageToken=page_token,
                )
                .execute()
            )
            print(response)
            for file in response.get("files", []):
                # Save the file ID and modified time
                files.append({"id": file["id"], "modifiedTime": file["modifiedTime"]})
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


# Save the initial list of files
previous_files = get_folder_contents()

# Set up a loop to check for changes every 60 seconds
while True:
    # Get the current list of files
    current_files = get_folder_contents()

    # Compare the lists and print a message for any new or modified files
    for file in current_files:
        print(f'Checking file: {file["id"]}')
        if file not in previous_files:
            print(f'------ New file: {file["id"]}')

    break
