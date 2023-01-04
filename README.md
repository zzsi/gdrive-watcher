`gdrive-watcher` is a library for watching file updates to a google drive folder.

[![PyPI version](https://badge.fury.io/py/gdrive-watcher.svg)](https://badge.fury.io/py/gdrive-watcher)

Set the environment variable for your google service account:

export GOOGLE_APPLICATION_CREDENTIALS="<path to your google service account file>.json"

In the service account JSON file, look for "client_email". Add this email address to the folder you like to watch, or its parent folder.

Example usage:

```python
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from gdrive_watcher import GDriveWatcher
from gdrive_watcher.gdrive_reader import GDriveReader

load_dotenv()

folder_id = os.environ["FOLDER_ID"]
watcher = GDriveWatcher(
    folder_id=folder_id,
    watch_start_time=datetime.now() - timedelta(days=5), # feel free to change this
)
reader = GDriveReader()
for event in watcher.watch():
    print("-", event)
    if not event.is_folder:
        print("content:", reader.read_by_file_id(event.file_id))
```

For debugging, run

```
python gdrive_watcher/poll.py 
```

Note: there may be a timing issue if your timezone is different from the timezone of your google drive account.