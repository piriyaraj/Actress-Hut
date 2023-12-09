import cv2

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
    if duration > 60 or width != 1080 or height != 1920 :
        return False
    return True
# Example usage
video_path = r'D:\Youtube\Actress HUB\post_rashmika_mandanna_3249644338181046718\2023-12-03_12-51-49_UTC.mp4'
width, height, fps, duration, aspect_ratio = get_video_info(video_path)
print(isItReel(width, height, fps, duration, aspect_ratio))
