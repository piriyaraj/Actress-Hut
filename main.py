import os
import sqlite3
import time
import utils.tools as tools
import os
import shutil
from discordwebhook import Discord

import utils.videoUploader as videoUploader

import cv2

import datetime

videoUploader.get_authenticated_service()
current_datetime = datetime.datetime.now()
print("Current Date and Time:", current_datetime)


def get_video_info(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        print("Error: Could not open the video file.")
        return

    # Get the width and height of the video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Get the frames per second (FPS) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Get the total number of frames in the video
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the duration of the video in seconds
    duration_seconds = frame_count / fps

    # Calculate the aspect ratio
    aspect_ratio = width / height

    # Release the video capture object
    cap.release()

    return width, height, fps, duration_seconds, aspect_ratio


def isItReel(width, height, fps, duration, aspect_ratio):
    if duration > 59 or aspect_ratio != 0.5625:
        return False
    return True


if not os.path.exists('media/videos'):
    os.makedirs('media/videos')


# Check if the database file exists
if not os.path.exists('src/database/data.sqlite3'):
    # Create a new database file if it doesn't exist
    conn = sqlite3.connect('src/database/data.sqlite3')
    cursor = conn.cursor()

    # Create the table with 'instaId' and 'modified_date' columns
    cursor.execute('''
        CREATE TABLE data (
            instaId TEXT PRIMARY KEY,
            modified_date TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database 'data.sqlite3' created successfully.")
else:
    print("Database 'data.sqlite3' already exists.")


def DiscordNotification(Msg):
    webHookUrl = "https://discord.com/api/webhooks/1132597585824202813/8XDNjpwwOIsistL4nThyY7NjVo67UVHckbtOAAdGAf96_TZ7dTS3tOpDmle646rF_ZDX"
    discord = Discord(url=webHookUrl)
    discord.post(content=Msg)


def uploader(videoPath, user, hour):
    video = videoPath
    userId = videoPath.split("post_")[1].split("_")[0]
    try:
        title = f"Trending {user} ❤️ latest video #shorts #trending #{userId}"
        description = title + f'''
        {title}
        Welcome to this captivating video featuring an in-depth look into the life and career of the talented actress {user}. Join us as we delve into the remarkable journey of {user}, a true icon in the world of entertainment.

        In this video, we explore the extraordinary talent, dedication, and passion that have propelled {user} to the forefront of the acting industry. From her early beginnings to her rise to stardom, witness the inspiring story of {user}'s pursuit of her dreams and the obstacles she overcame along the way.

        Through captivating interviews, behind-the-scenes footage, and memorable clips from her most acclaimed performances, this video offers an exclusive glimpse into the world of {user}. Discover the versatility and depth of {user}'s acting skills as we showcase her ability to portray a wide range of characters with authenticity and brilliance.

        Prepare to be inspired as we highlight the impact {user} has made in the entertainment industry and the hearts of her fans worldwide. From her captivating screen presence to her commitment to meaningful storytelling, {user} continues to captivate audiences with her talent and charm.

        Join us on this mesmerizing journey as we celebrate the accomplishments and contributions of actress {user}. Whether you're a devoted fan or new to {user}'s work, this video promises to provide an immersive experience that celebrates her artistry and the indelible mark she has made in the world of acting.

        Don't miss out on this opportunity to discover the magic of {user}'s performances and gain insights into her inspiring journey. Like, comment, and share this video to spread the word about the incredible talent and inspiration that actress {user} embodies.

        #{user} #Actress #Inspiration #Celebrity #Film #Entertainment
        '''
        keywords = []
        # upload (hour) hours once
        videoUploader.uploadVideos(
            user, videoPath, title, description, keywords, hour*60)

        return True, "Video was successfully uploaded"
    except Exception as e:
        print(e)
        return False, e


def noVideoHandler():
    tools.startDownload()


try:
    with open(os.path.abspath("src/time.txt"), "r") as file:
        hour = int(file.readline())
except:
    hour = 3


# exit()

folderPath = [file for file in os.listdir() if file.startswith("post_")]
if len(folderPath) == 0:
    try:
        noVideoHandler()
    except Exception as e:
        DiscordNotification(f"ACTRESS Hut(YT): {e}")
    finally:
        time.sleep(5)
folderPath = [file for file in os.listdir() if file.startswith("post_")]
if len(folderPath) == 0:
    print("No new folder path found")
    DiscordNotification(f"ACTRESS Hut(YT): No new video available")
    time.sleep(5)
    exit()
    # folderPath = [file for file in os.listdir() if file.startswith("post_")]
    # if len(folderPath) == 0:
    #     print("No new folder path found")

    #     exit()

folderPath = [file for file in os.listdir() if file.startswith("post_")]
no_of_video = 1
if no_of_video > len(folderPath):
    no_of_video = len(folderPath)

count = 0
while count < no_of_video:
    i = count
    print(folderPath[i])
    videoList = [f for f in os.listdir(folderPath[i]) if f.endswith('.mp4')]
    if len(videoList) == 0:
        shutil.rmtree(folderPath[i])
        exit()

    videoPath = os.path.abspath(os.path.join(folderPath[i], videoList[0]))

    width, height, fps, duration, aspect_ratio = get_video_info(videoPath)
    print(width, height, fps, duration, aspect_ratio)
    if not (isItReel(width, height, fps, duration, aspect_ratio)):
        print("Video is not a reel")
        shutil.rmtree(folderPath[i])
        if no_of_video < len(folderPath):
            no_of_video += 1
        count += 1
        continue

    profile_name_filepath = os.path.join(folderPath[i], 'profile_name.txt')
    with open(profile_name_filepath, 'r', encoding='utf8') as file:
        profile_name = file.readline().strip()

    count += 1
    status, msg = uploader(videoPath, profile_name, hour)
    # only msg sent when the appear error
    if not status:
        DiscordNotification(f"ACTRESS Hut(YT): {msg}")
        break
    else:
        DiscordNotification(f"ACTRESS Hut(YT): Video uploaded successfully")
        shutil.rmtree(folderPath[i])
        with open(os.path.abspath("src/time.txt"), "w") as file:
            hour += 3
            if hour == 21:
                hour = 3
            file.write(str(hour))
