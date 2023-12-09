import os
import random
import sqlite3
import time
import requests
from datetime import datetime
from instaloader import Instaloader, LoginRequiredException, Profile
from moviepy.editor import ImageClip, concatenate_videoclips,AudioFileClip
from PIL import Image
import shutil
import numpy as np
import re

def downloadVideo(username,threshold_time):
    error = False
    count = 0
    try:
        # Create an instance of Instaloader
        L = Instaloader()

        # Load the profile
        profile = Profile.from_username(L.context, username)

        profile_name = profile.full_name
        for post in profile.get_posts():
            # Check if the post was uploaded after the threshold time and if it's not a video
            if post.date > threshold_time:
                # print(post,post.date,post.is_video)
                if post.is_video:
                    post_folder = f"post_{username}_{post.mediaid}"
                    os.makedirs(post_folder, exist_ok=True)
                    print(f'          >> downloading: post_{post.mediaid}')
                    L.download_post(post, post_folder)
                    # Save the post caption as a text file
                    caption = post.caption
                    caption_filepath = os.path.join(post_folder, "caption.txt")
                    with open(caption_filepath, "w", encoding="utf-8") as f:
                        f.write(caption)
                        
                    profile_name_filepath = os.path.join(post_folder, "profile_name.txt")
                    with open(profile_name_filepath, "w", encoding="utf-8") as f:
                        f.write(profile_name)
                    time.sleep(5)
                    count += 1
            else:
                print("Process finished")
                break
    except Exception as e:
        print("Error(downloadVideo): " + str(e))
        error = True
    return error, count

def fetch_data_as_dict():
    conn = sqlite3.connect('src/database/data.sqlite3')
    cursor = conn.cursor()

    # Fetch data ordered by 'modified_date'
    cursor.execute('SELECT instaId, modified_date FROM data ORDER BY modified_date ASC')
    rows = cursor.fetchall()

    # Create a dictionary to store the data
    data_dict = {}
    for row in rows:
        insta_id, modified_date = row
        data_dict[insta_id] = modified_date

    conn.close()
    return data_dict


def update(data):
    conn = sqlite3.connect('src/database/data.sqlite3')
    cursor = conn.cursor()

    for insta_id, new_date in data.items():
        # Update the 'modified_date' for the given 'instaId'
        cursor.execute('INSERT OR REPLACE INTO data (instaId, modified_date) VALUES (?, ?)', (insta_id, new_date))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
def videoMaker(instaId, pathFolder):
    # Get the first line from the text file as the video name
    text_file_path = os.path.join(pathFolder, 'caption.txt')
    with open(text_file_path, 'r', encoding='utf8') as file:
        video_name = file.readline().strip()
    video_name = re.sub(r'[^a-zA-Z0-9 ]', '', video_name)[:100]
    profile_name_filepath = os.path.join(pathFolder, 'profile_name.txt')
    with open(profile_name_filepath, 'r', encoding='utf8') as file:
        profile_name = file.readline().strip()
    # Create a temporary blank image with the desired size
    temp_image = Image.open('src/Actress Area template.png')  # White background

    # Get all image files from the folder
    image_files = [file for file in os.listdir(pathFolder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()  # Sort the files to maintain order

    # Create a list of resized image clips with overlay
    clips = []
    for image_file in image_files:
        image_path = os.path.join(pathFolder, image_file)
        image = Image.open(image_path)

        # Resize the image to fit within the temp_image while maintaining the aspect ratio and original ratio
        width, height = image.size
        image_ratio = width / height
        temp_ratio = temp_image.width / temp_image.height

        if image_ratio > temp_ratio:
            temp_height = int(temp_image.width * (height/width))
            resized_image = image.resize((temp_image.width, temp_height))
        else:
            new_width = int(temp_image.height / (width/height))
            resized_image = image.resize((new_width, temp_image.height))

        # Calculate the position to paste the resized image onto the temporary image (white background)
        position = ((temp_image.width - resized_image.width) // 2, (temp_image.height - resized_image.height) // 2)
        temp_image.paste(resized_image, position)

        # Convert PIL Image to numpy array
        image_array = np.array(temp_image)

        # Create an ImageClip with the numpy array
        image_clip = ImageClip(image_array, duration=3)
        clips.append(image_clip)

    # select random music
    audio_path = selectRandomMusic()
    audio_clip = AudioFileClip(audio_path)
    # Concatenate the image clips into a single video clip
    final_clip = concatenate_videoclips(clips)
    audio_clip = audio_clip.subclip(0, final_clip.duration)
    final_clip = final_clip.set_audio(audio_clip)
    outputPath = "output video"
    os.makedirs(outputPath, exist_ok=True)
    # Set the video output path and write the video file
    video_output_path = os.path.join(outputPath, f'{profile_name} - {video_name}.mp4')
    
    final_clip.write_videofile(video_output_path, codec='libx264', fps=24, threads=4, preset='ultrafast')  # Write the video file

def remove_emojis(text):
    # Regular expression pattern to match emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"
        "]+"
    )
    # Remove emojis using the regex pattern
    return emoji_pattern.sub('', text)

def startDownload():
    instaData = fetch_data_as_dict()
    for instaId,value in instaData.items():
        print(f"=========> {instaId} <=========== ")
        datetime_obj = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
        current_time = datetime.now()
        time_difference = current_time - datetime_obj
        hours_difference = int(time_difference.total_seconds() / 3600)
        if hours_difference<=6:
            continue
        error,count = downloadVideo(instaId,datetime_obj)
        print("Donwloaded videos: ",count)
        if count >= 0:
            update({instaId:datetime.now().isoformat()})
        if error:
            return
        
            

if __name__ == "__main__":
    datetime_obj = datetime.strptime("2023-11-10T12:05:04.978896", '%Y-%m-%dT%H:%M:%S.%f')
    downloadVideo("athulyaofficial",datetime_obj)
    # print(fetch_data_as_dict())
    # updateImages()
    # startDownload()