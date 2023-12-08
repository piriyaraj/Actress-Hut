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

    # Release the video capture object
    cap.release()

    return width, height, fps, duration_seconds


# Example usage
video_path = r'D:\Youtube\Actress HUB\post_losliyamariya96_3234986523816973398\2023-11-13_07-28-53_UTC.mp4'
width, height, fps, duration = get_video_info(video_path)
print(f"Video Dimensions: {width} x {height}")
print(f"Frames Per Second (FPS): {fps}")
print(f"Video Duration: {duration:.2f} seconds")
