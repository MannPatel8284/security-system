import cv2
import numpy as np
import smtplib
from email.message import EmailMessage
import time
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Use the default camera index '0' for the MacBook's built-in camera.
CAMERA_URL = 0

# Email settings for notifications (loaded from .env file for security)
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL" )
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # Port for TLS

# Delay between notifications in seconds to prevent spamming
NOTIFICATION_DELAY = 60

# Motion detection sensitivity (lower = more sensitive, higher = less sensitive)
MOTION_THRESHOLD = 25
MIN_CONTOUR_AREA = 500

# --- Function to Send Email Notification ---
def send_notification(subject, body):
    """
    Sends an email notification with the given subject and body.
    """
    # Check if password is set
    if not SENDER_PASSWORD:
        print("Error: SENDER_PASSWORD not set in .env file")
        return False
    
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        print(f"Attempting to connect to SMTP server: {SMTP_SERVER} on port {SMTP_PORT}...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            print("TLS connection started. Logging in...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("Login successful. Sending message...")
            server.send_message(msg)
            print("✓ Notification email sent successfully!")
            return True
    except smtplib.SMTPAuthenticationError:
        print("✗ Error: SMTP Authentication Failed.")
        print("  - Ensure you're using a Google App Password, not your regular account password")
        print("  - Check that SENDER_EMAIL and SENDER_PASSWORD are correct in .env file")
        return False
    except smtplib.SMTPException as e:
        print(f"✗ Error sending email: {e}")
        return False
    except Exception as e:
        print(f"✗ An unexpected error occurred: {e}")
        return False

# --- Main Program ---
try:
    # Open the video stream from the camera
    cap = cv2.VideoCapture(CAMERA_URL)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("✗ Error: Could not open video stream. Check camera permissions.")
        exit()

    print("✓ Camera opened successfully")

    # Read the first frame to use as the initial background reference
    ret, frame1 = cap.read()
    if not ret:
        print("✗ Error: Could not read from camera")
        cap.release()
        exit()

    # Convert the first frame to grayscale and apply a blur to reduce noise
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

    # Initialize a variable to store the last time a notification was sent
    last_notification_time = 0

    print("=" * 60)
    print("✓ Motion detection started")
    print("=" * 60)
    print("Controls:")
    print("  - Press 'q' to quit")
    print("  - Press 's' to save a snapshot")
    print("=" * 60)

    # --- Main Loop ---
    frame_count = 0
    while True:
        # Read the next frame from the video stream
        ret, frame2 = cap.read()
        if not ret:
            print("End of video stream.")
            break

        frame_count += 1

        # Convert the new frame to grayscale and apply a blur
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

        # Calculate the absolute difference between the two grayscale frames
        diff = cv2.absdiff(gray1, gray2)

        # Apply a threshold to the difference image
        thresh = cv2.threshold(diff, MOTION_THRESHOLD, 255, cv2.THRESH_BINARY)[1]

        # Dilate the thresholded image to fill in holes and make contours more visible
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        motion_count = 0

        # Loop through each contour detected
        for contour in contours:
            # If the contour area is too small, it's probably just noise
            if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
                continue

            motion_detected = True
            motion_count += 1

            # Get the bounding box of the contour (x, y, width, height)
            (x, y, w, h) = cv2.boundingRect(contour)

            # Draw a green rectangle around the moving object
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Add timestamp and status to the frame
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame2, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if motion_detected:
            status_text = f"MOTION DETECTED ({motion_count} objects)"
            status_color = (0, 0, 255)  # Red
            cv2.putText(frame2, status_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)

        # Check for motion and notification cooldown
        if motion_detected and (time.time() - last_notification_time) > NOTIFICATION_DELAY:
            # Create the email content
            subject = "🚨 Motion Detected!"
            body = f"Motion was detected by the camera at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n\nNumber of objects detected: {motion_count}"

            # Send the notification
            if send_notification(subject, body):
                last_notification_time = time.time()
                print(f"[{timestamp}] Alert sent! Motion with {motion_count} object(s) detected.")

        # Display the output frame
        cv2.imshow("Security Feed", frame2)
        cv2.imshow("Motion Detection", thresh)

        # Update the background frame ONLY when no motion is detected
        # This prevents constant green rectangles and improves accuracy
        if not motion_detected:
            gray1 = gray2

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("\n" + "=" * 60)
            print("Exiting motion detection...")
            print("=" * 60)
            break
        elif key == ord("s"):
            # Save a snapshot
            snapshot_filename = f"snapshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(snapshot_filename, frame2)
            print(f"✓ Snapshot saved: {snapshot_filename}")

finally:
    # Release the video capture object and close all OpenCV windows
    if 'cap' in locals() and cap.isOpened():
        cap.release()
        print("✓ Camera released")
    
    cv2.destroyAllWindows()
    print("✓ All windows closed")
    print("Motion detection stopped.")