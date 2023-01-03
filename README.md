<package-name> is a library for ....

Set the environment variable for your google service account:

export GOOGLE_APPLICATION_CREDENTIALS="<path to your google service account file>.json"

In the service account JSON file, look for "client_email". Add this email address to the folder you like to watch, or its parent folder.

Example usage:

```
python gdrive_watcher/poll.py
```

or

```
python -m gdrive_watcher
```

Note: there may be a timing issue if your timezone is different from the timezone of your google drive account.