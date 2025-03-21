from picamera2 import Picamera2, Preview
import time
import cv2
import RPi.GPIO as GPIO
import os
import subprocess

# Run the wlrctl command to move the pointer
def move_pointer():
    try:
        subprocess.run(["/usr/local/bin/wlrctl", "pointer", "move", "1920", "1080"], check=True, text=True)
        print("Pointer moved to (1920, 1080).")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print(f"stderr: {e.stderr}")
        print(f"stdout: {e.stdout}")



# SETUP GPIO
BUTTON_GPIO = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set the save path to the desktop
desktop_path = os.path.expanduser("/home/skngh/Desktop/photo.jpg")

# Initialize Picamera2
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (853, 480)})
picam2.configure(camera_config)
cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


picam2.start()

freezeFrame = False
frozenImage = None
canTakePhoto = True
photoStartTime = 0
freezeDelay = 4  # Seconds
startTime = False
timer = 0


if os.path.exists(desktop_path):
    frozenImage = cv2.imread(desktop_path)
    if frozenImage is not None:
        freezeFrame = True
        print(f"Loaded existing photo from {desktop_path}")
        
# Call the function to move the pointer
move_pointer()

while True:
    # Capture a frame from the camera
    frame = picam2.capture_array()

    key = cv2.waitKey(1) & 0xFF
    
    button_pressed = GPIO.input(BUTTON_GPIO) == GPIO.LOW

    # Take photo on spacebar press
    if button_pressed:
        if canTakePhoto:
            freezeFrame = None
            photoStartTime = time.time()
            startTime = True
            canTakePhoto = False

    if startTime:
        timer = abs(int((time.time() - photoStartTime) - freezeDelay))
        if time.time() - photoStartTime >= freezeDelay:
            freezeFrame = True
            frozenImage = frame
            canTakePhoto = True
            startTime = False
            # Save the photo, overwriting the previous one (so it'll be displayed next time if you turn off the pi)
            cv2.imwrite(desktop_path, frozenImage)
    kernel_size = 21
    if freezeFrame and frozenImage is not None:
        # APPLY ANY SEPERATE FILTERING YOU WANT HERE!

        # Apply Gaussian Blur to the frozen frame
        blurred_frame = cv2.GaussianBlur(frozenImage, (kernel_size, kernel_size), 0)

        # Convert to grayscale
        gray = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding
        _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        frame_to_show = thresholded
        
        
    else:
        frame_to_show = frame

    # Add text in the bottom-left corner
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f"{int(timer)}" if startTime else ""
    position = (10, frame.shape[0] - 10)  # Bottom-left corner
    cv2.putText(frame_to_show, text, position, font, 5, (0, 0, 255), 10, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Camera', frame_to_show)

    # Exit on 'q'
    if key == ord('q'):
        break

# Clean up
picam2.stop()
cv2.destroyAllWindows()
