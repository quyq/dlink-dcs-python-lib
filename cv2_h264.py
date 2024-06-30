import cv2
import os
from dlinkdcs import DlinkDCSCamera as ipcam

# URL of the H.264 video stream
CAM_HOST = os.environ.get('CAM_HOST') or ''
CAM_PORT = os.environ.get('CAM_PORT', 80)
CAM_USER = os.getenv('CAM_USER', 'admin')
CAM_PASS = os.getenv('CAM_PASS', '')

ipcam = ipcam(CAM_HOST, CAM_USER, CAM_PASS, CAM_PORT)
r = ipcam.get_ptz()
print(r)
#set_ptz(self, pan=167, tilt=25, zoom=0):
"""
pan -- 0 to 336 (default: 167)
tile -- 0 to 106 (default: 25)
"""
pan_max=336
tile_max=106
zoom_max=10
pan=167
tile=25
zoom=0
r = ipcam.set_ptz(pan, tile, zoom)

# URL of the video stream
stream_url = f'http://{CAM_USER}:{CAM_PASS}@{CAM_HOST}:{CAM_PORT}/video.cgi'

# Create a VideoCapture object
cap = cv2.VideoCapture(stream_url)

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

        # Wait for a key press and extract the last byte
        key = cv2.waitKeyEx(1)

        # Check if 'q' is pressed to exit
        if key&0xFF == ord('q'):
            break

        # Arrow keys handling
        if key>>16 == 0x25: # Left arrow
            pan -= 5
            if pan<0: pan=0
        elif key>>16 == 0x26: # Up arrow
            tile += 5
            if tile>tile_max: tile=tile_max
        elif key>>16 == 0x27: # Right arrow
            pan += 5
            if pan>pan_max: pan=pan_max
        elif key>>16 == 0x28: # Down arrow
            tile -= 5
            if tile<0: tile=0
        elif key&0xFF == 61:  # '='
            zoom += 1
            if zoom>zoom_max: zoom=zoom_max
        elif key&0xFF == 45:  # '-'
            zoom -= 1
            if zoom<0: zoom=0
        else: key = 0
        if key!=0:
            r = ipcam.set_ptz(pan, tile, zoom)
            #print(r)
# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()