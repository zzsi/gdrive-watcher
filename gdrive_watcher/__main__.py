if __name__ == "__main__":
    from datetime import datetime, timedelta
    from dotenv import load_dotenv
    import os
    from gdrive_watcher import GDriveWatcher
    from gdrive_watcher.gdrive_reader import GDriveReader

    load_dotenv()

    folder_id = os.environ["FOLDER_ID"]
    watcher = GDriveWatcher(
        folder_id=folder_id,
        watch_start_time=datetime.now() - timedelta(days=5),
    )
    reader = GDriveReader()
    for event in watcher.watch():
        print("-", event)
        if not event.is_folder:
            print("content:", reader.read_by_file_id(event.file_id))

    # TODO: try deleting a file manually, and see if the file still shows.
