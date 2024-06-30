import ffmpegcv    # pip install ffmpegcv
import cv2
import os

# URL of the H.264 video stream
CAM_HOST = os.environ.get('CAM_HOST') or ''
CAM_PORT = os.environ.get('CAM_PORT', 80)
CAM_USER = os.getenv('CAM_USER', 'admin')
CAM_PASS = os.getenv('CAM_PASS', '')

# URL of the video stream
stream_url = f'http://{CAM_USER}:{CAM_PASS}@{CAM_HOST}:{CAM_PORT}/video.cgi'

# Create a VideoCapture object
cap = ffmpegcv.VideoCaptureStream(stream_url)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream.")
else:
    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Display the resulting frame
            cv2.imshow('Video Stream', frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()