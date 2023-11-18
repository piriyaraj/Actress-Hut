import datetime
import os
import random
import time
import pytz
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import httplib2
from utils.database import Database


def get_authenticated_service():
    CLIENT_SECRETS_FILE = os.path.abspath("src/credentials/client_secret.json")
    YOUTUBE_UPLOAD_SCOPE = ('https://www.googleapis.com/auth/youtubepartner', 'https://www.googleapis.com/auth/youtube',
                            'https://www.googleapis.com/auth/youtube.force-ssl', 'https://www.googleapis.com/auth/youtube.upload')
    MISSING_CLIENT_SECRETS_MESSAGE = f"""WARNING: Please configure OAuth 2.0"""

    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("src\credentials\storage-oauth2.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    return build("youtube", "v3", http=credentials.authorize(httplib2.Http()))


def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error)
    while response is None:
        print("=== Video uploding (wait until uploading finish) ===")
        try:
            # print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print(
                        f"Video id {response['id']} was successfully uploaded.")
                    return response['id']
                else:
                    exit(
                        f"The upload failed with an unexpected response: {response}")
        except HttpError as e:
            RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f"A retriable error occurred: {e}"

        if error is not None:
            print(error)
            MAX_RETRIES = 10
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print(f"Sleeping {sleep_seconds} seconds and then retrying...")
            time.sleep(sleep_seconds)


def create_playlist(playListName, description):
    youtube = get_authenticated_service()
    resource = {
        'snippet': {
            'title': playListName,
            'description': description
        },
        'status': {
            'privacyStatus': 'public'
        }
    }
    try:
        response = youtube.playlists().insert(
            part='snippet,status',
            body=resource
        ).execute()
        playlist_id = response['id']
        print(
            f"Playlist '{playListName}' created successfully with id '{playlist_id}'")
    except HttpError as error:
        print(f"An HTTP error {error.resp.status} occurred: {error.content}")
        playlist_id = None
    return playlist_id


def add_video_to_playlist(videoID, playlistID):
    youtube = get_authenticated_service()
    try:
        add_video_request = youtube.playlistItems().insert(
            part="snippet",
            body={
                'snippet': {
                    'playlistId': playlistID,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': videoID
                    }
                    # 'position': 0
                }
            }
        ).execute()
    except Exception as e:
        print("Error(Adding playlist to video:)", str(e))


def uploadVideos(nameOfId: str, filePath: str, title: str, description: str, keywords: list, delay: int, category="22"):
    youtube = get_authenticated_service()
    print("==== Trying to upload:",title," ===")
    options = {
        "file": filePath,
        "title": title,
        "description": description,
        "category": category,
        "keywords": keywords,
        "privacyStatus": 'private'
    }
    tags = [nameOfId,"latest "+nameOfId ,"trending", "Actress video", "Celebrity",
            "whatsapp status", "shorts", "cute", "photo shoots", "story", "Hot "+nameOfId]
    local_tz = pytz.timezone('Asia/Colombo')
    scheduled_time = datetime.datetime.now() + datetime.timedelta(minutes=delay)

    if options['keywords']:
        tags = options['keywords']
    # print(scheduled_time.strftime('%Y-%m-%dT%H:%M:%SZ'))
    body = dict(
        snippet=dict(
            title=options['title'],
            description=options['description'],
            tags=tags,
            categoryId=options['category']
        ),
        status=dict(
            privacyStatus=options['privacyStatus'],
            publishAt=scheduled_time.isoformat() + 'Z'
        )
    )
    chunksize = -1

    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(
            options['file'], chunksize=chunksize, resumable=True)
    )
    insert_request.notifySubscribers = True
    video_id = resumable_upload(insert_request)
    time.sleep(5)
    database = Database()

    tag = nameOfId
    tag_id = database.getPlayListId(tag)
    if tag_id == None:
        description = f"""Welcome to the official YouTube playlist featuring short videos of the talented celebrity actress {nameOfId}. Dive into this captivating collection of short clips that showcase the versatility and charm of {nameOfId}'s performances. From memorable scenes to behind-the-scenes snippets, this playlist offers an exciting glimpse into the world of {nameOfId}.

        Get ready to be mesmerized by {nameOfId}'s captivating talent and charisma in these bite-sized videos. Whether you're a dedicated fan or new to {nameOfId}'s work, this playlist is a must-watch for anyone who appreciates exceptional acting skills and on-screen magic.

        Join us on this exciting journey through {nameOfId}'s career as we curate the best short videos highlighting her remarkable talent. From emotional moments to comedic brilliance, each video in this playlist is carefully selected to provide a delightful viewing experience.

        Subscribe to our channel to stay updated with the latest additions to this playlist, as we continue to add more captivating short videos featuring the incredible celebrity actress {nameOfId}. Prepare to be entertained, inspired, and enchanted by {nameOfId}'s magnetic presence in these remarkable short clips.

        Note: All videos in this playlist are owned by their respective creators. Please support and follow {nameOfId} on her official social media accounts for more updates and exciting projects.

        #{nameOfId} #CelebrityActress #ShortVideos #Entertainment
        """
        time.sleep(10)
        tag_id = create_playlist(tag, description=description)
        database.setPlayListId(tag_id, tag)
    time.sleep(10)
    add_video_to_playlist(video_id, tag_id)
    pass


if __name__ == '__main__':
    get_authenticated_service()