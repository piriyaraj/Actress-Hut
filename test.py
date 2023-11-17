import os
folderPath = [file for file in os.listdir() if file.startswith("post_")]

videoPath = [f for f in os.listdir(folderPath[0]) if f.endswith('.mp4')]
if len(videoPath) == 0:
    exit()
videoList = [f for f in os.listdir(folderPath[0]) if f.endswith('.mp4')]
if len(videoList) == 0:
    exit()

videoPath = os.path.abspath(os.path.join(folderPath[0],videoList[0]))
profile_name_filepath = os.path.join(folderPath[0], 'profile_name.txt')
with open(profile_name_filepath, 'r', encoding='utf8') as file:
    profile_name = file.readline().strip()
print(videoPath.split("post_")[1].split("_")[0])