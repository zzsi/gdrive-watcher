if __name__ == "__main__":
    from datetime import datetime, timedelta
    from dotenv import load_dotenv
    import os
    from gdrive_watcher.gdrive_poll_watcher import GDrivePollWatcher

    load_dotenv()

    folder_id = os.environ["FOLDER_ID"]
    watcher = GDrivePollWatcher(
        folder_id=folder_id,
        watch_start_time=datetime.now() - timedelta(days=5),
    )
    for event in watcher.watch():
        print(event)

    # TODO: try deleting a file manually, and see if the file still shows.
