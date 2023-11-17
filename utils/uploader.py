import datetime
import os
import shutil

import utils.videoUploader as videoUploader

# if Folder Temp/Videos and Folder Temp/Images not exist, create them
if not os.path.exists('Temp/Videos'):
    os.makedirs('Temp/Videos')
if not os.path.exists('Temp/Images'):
    os.makedirs('Temp/Images')
    
def moveFile(source_path):
    destination_path = os.path.join("Temp/Videos", source_path.split("\\")[-1])
    shutil.move(source_path, destination_path)

def main():
    # get all video files from folder called "output video"
    videos = os.listdir("output video")
    for video in videos:
        title = os.path.splitext(video)[0][:100]
        user = title.split(" - ")[0]
        description = title + f'''
        Welcome to this captivating video featuring an in-depth look into the life and career of the talented actress {user}. Join us as we delve into the remarkable journey of {user}, a true icon in the world of entertainment.

        In this video, we explore the extraordinary talent, dedication, and passion that have propelled {user} to the forefront of the acting industry. From her early beginnings to her rise to stardom, witness the inspiring story of {user}'s pursuit of her dreams and the obstacles she overcame along the way.

        Through captivating interviews, behind-the-scenes footage, and memorable clips from her most acclaimed performances, this video offers an exclusive glimpse into the world of {user}. Discover the versatility and depth of {user}'s acting skills as we showcase her ability to portray a wide range of characters with authenticity and brilliance.

        Prepare to be inspired as we highlight the impact {user} has made in the entertainment industry and the hearts of her fans worldwide. From her captivating screen presence to her commitment to meaningful storytelling, {user} continues to captivate audiences with her talent and charm.

        Join us on this mesmerizing journey as we celebrate the accomplishments and contributions of actress {user}. Whether you're a devoted fan or new to {user}'s work, this video promises to provide an immersive experience that celebrates her artistry and the indelible mark she has made in the world of acting.

        Don't miss out on this opportunity to discover the magic of {user}'s performances and gain insights into her inspiring journey. Like, comment, and share this video to spread the word about the incredible talent and inspiration that actress {user} embodies.

        #{user} #Actress #Inspiration #Celebrity #Film #Entertainment
        '''
        filePath = os.path.abspath("output video/"+video)
        keywords = []
        # upload 3 hours once
        videoUploader.uploadVideos(user,filePath, title, description, keywords, 3*60*(videos.index(video)+1))
        moveFile(filePath)

if __name__ == "__main__":
    main()