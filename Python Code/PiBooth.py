from picamera2 import Picamera2, Preview
import time
import cv2
import RPi.GPIO as GPIO
import os

# SETUP GPIO
BUTTON_GPIO = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set the save path to the desktop
desktop_path = os.path.expanduser("/home/pi/Desktop/photo.jpg")

# Initialize Picamera2
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (853, 480)})
picam2.configure(camera_config)

# Configure OpenCV window for fullscreen display
cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Start the camera
picam2.start()

# Initialize variables
freezeFrame = False
frozenImage = None
canTakePhoto = True
photoStartTime = 0
FREEZE_DELAY = 4  # Seconds
startTime = False
timer = 0

# Load existing photo if available
if os.path.exists(desktop_path):
    frozenImage = cv2.imread(desktop_path)
    if frozenImage is not None:
        freezeFrame = True
        print(f"Loaded existing photo from {desktop_path}")
    else:
        print(f"Failed to load photo from {desktop_path}")

while True:
    # Capture a frame from the camera
    frame = picam2.capture_array()

    # Check for button press
    button_pressed = GPIO.input(BUTTON_GPIO) == GPIO.LOW

    # Handle photo capture logic
    if button_pressed and canTakePhoto:
        freezeFrame = None
        photoStartTime = time.time()
        startTime = True
        canTakePhoto = False

    if startTime:
        # Calculate countdown timer
        timer = abs(int((time.time() - photoStartTime) - FREEZE_DELAY))
        if time.time() - photoStartTime >= FREEZE_DELAY:
            freezeFrame = True
            frozenImage = frame
            canTakePhoto = True
            startTime = False
            # Save the photo to desktop, overwriting the previous one (so it'll be displayed next time if you turn off the pi)
            cv2.imwrite(desktop_path, frozenImage)

    # Apply filtering to the frozen frame
    KERNEL_SIZE = 21
    if freezeFrame and frozenImage is not None:
        # APPLY FILTERS HERE

        blurred_frame = cv2.GaussianBlur(frozenImage, (KERNEL_SIZE, KERNEL_SIZE), 0)
        gray = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)

        # Apply binary thresholding
        _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        frame_to_show = thresholded
    else:
        frame_to_show = frame

    # Add countdown text to the frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f"{int(timer)}" if startTime else ""
    position = (10, frame.shape[0] - 10)  # Bottom-left corner
    cv2.putText(frame_to_show, text, position, font, 5, (0, 0, 255), 10, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Camera', frame_to_show)

    # Exit the program when 'q' is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Clean up resources
picam2.stop()
cv2.destroyAllWindows()
