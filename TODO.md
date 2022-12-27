## Authentication

Share the folder or file you want to access with the GCP service account's email address. You can do this by going to the Google Drive folder or file, clicking the "Share" button, and adding the service account's email address as a "Can edit" user.


## By Polling

- Set up a Google Drive API key and install the Google API client library for Python. You can find instructions for this in the Google Drive API documentation.

- Use the Google API client library to authenticate your script and authorize it to access your Google Drive account.

- Use the Google Drive API to list the files in the folder you want to watch. You can use the Files.list method to do this.

- Save the list of files and their metadata (such as their file IDs and modified times) to a local file or database.

## By Push notification

- Use the Google Cloud client library to authenticate your script and authorize it to access the Cloud Pub/Sub API.

- Use the google.cloud.pubsub_v1 module to create a publisher client and a topic.

- Use the Changes.watch method to set up a push notification that sends a request to a specified URL whenever a change occurs in a specific folder.

- In the server that receives the notifications, use the publisher client to send a message to the topic whenever a change is detected.

## References

- [blog](https://www.clairvoyant.ai/blog/enabling-google-drive-api-push-notifications-with-pub-sub-messaging)