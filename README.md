`gdrive-watcher` is a library for watching file updates to a google drive folder.

Set the environment variable for your google service account:

export GOOGLE_APPLICATION_CREDENTIALS="<path to your google service account file>.json"

In the service account JSON file, look for "client_email". Add this email address to the folder you like to watch, or its parent folder.

Example usage:


```
python -m gdrive_watcher
```

or for debugging,

```
python gdrive_watcher/poll.py 
```

Note: there may be a timing issue if your timezone is different from the timezone of your google drive account.