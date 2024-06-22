import cv2
import requests
import numpy as np
import os

#print(os.environ['HOME'])
# ref https://stackoverflow.com/questions/4906977/how-can-i-access-environment-variables-in-python. Below has same effect
CAM_HOST = os.environ.get('CAM_HOST') or ''
CAM_PORT = os.environ.get('CAM_PORT', 80)
CAM_USER = os.getenv('CAM_USER', 'admin')
CAM_PASS = os.getenv('CAM_PASS', '')

# URL of the video stream
stream_url = f'http://{CAM_HOST}:{CAM_PORT}/video.cgi'

# Start a session
session = requests.Session()
response = session.get(stream_url, stream=True, auth=(CAM_USER, CAM_PASS))

# Check if the connection to the stream is successful
if response.status_code == 200:
    bytes_data = bytes()
    for chunk in response.iter_content(chunk_size=1024):
        bytes_data += chunk
        a = bytes_data.find(b'\xff\xd8')  # JPEG start
        b = bytes_data.find(b'\xff\xd9')  # JPEG end
        if a != -1 and b != -1:
            jpg = bytes_data[a:b+2]  # Extract the JPEG image
            bytes_data = bytes_data[b+2:]  # Remove the processed bytes
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow('Video Stream', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit loop if 'q' is pressed
                    break
    cv2.destroyAllWindows()
else:
    print("Failed to connect to the stream.")
