import cv2
import mediapipe as mp
import serial
import time

# Initialize serial communication (adjust COM port and baud rate as needed)
ser = serial.Serial('/dev/cu.usbserial-210', 9600)  # Replace with your correct port
time.sleep(2)  # Wait for serial to initialize

# Initialize the hand solution
handSolution = mp.solutions.hands
hands = handSolution.Hands()
mp_drawing = mp.solutions.drawing_utils

# Open the default camera
videoCap = cv2.VideoCapture(0)

# Main loop
while True:
    # Read a frame from the camera and flip it
    success, img = videoCap.read()
    img = cv2.flip(img, 1)
    if not success:
        break

    h, w, _ = img.shape  # Get image dimensions

    # Define the size of the color rectangles
    rectangle_width = 300
    rectangle_height = 300

    # Draw the red rectangle in the top-left corner
    cv2.rectangle(img, (0, 0), (rectangle_width, rectangle_height), (0, 0, 255), -1)
    cv2.putText(img, 'RED', (30, 180), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4, cv2.LINE_AA)

    # Draw the green rectangle in the top-right corner
    cv2.rectangle(img, (w - rectangle_width, 0), (w, rectangle_height), (0, 255, 0), -1)
    cv2.putText(img, 'GREEN', (w - 280, 180), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4, cv2.LINE_AA)

    # Draw the blue rectangle in the bottom-left corner
    cv2.rectangle(img, (0, h - rectangle_height), (rectangle_width, h), (255, 0, 0), -1)
    cv2.putText(img, 'BLUE', (30, h - 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4, cv2.LINE_AA)

    # Process hand landmarks
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    recHands = hands.process(img_rgb)

    # Check if a hand is detected
    if recHands.multi_hand_landmarks:
        for hand_landmarks in recHands.multi_hand_landmarks:
            # Extract the x and y coordinates of the index finger tip (landmark 8)
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            # Initialize RGB values
            red, green, blue = 0, 0, 0

            # Check if the hand is in the red rectangle
            if 0 <= x <= rectangle_width and 0 <= y <= rectangle_height:
                red = 255
                rgb_message = f"{red},{green},{blue}\n"
                ser.write(rgb_message.encode())
                print("Red zone detected")

            # Check if the hand is in the green rectangle
            elif (w - rectangle_width) <= x <= w and 0 <= y <= rectangle_height:
                green = 255
                rgb_message = f"{red},{green},{blue}\n"
                ser.write(rgb_message.encode())
                print("Green zone detected")

            # Check if the hand is in the blue rectangle
            elif 0 <= x <= rectangle_width and (h - rectangle_height) <= y <= h:
                blue = 255
                rgb_message = f"{red},{green},{blue}\n"
                ser.write(rgb_message.encode())
                print("Blue zone detected")

            # Draw hand landmarks
            mp_drawing.draw_landmarks(
                img,
                hand_landmarks,
                handSolution.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=18, circle_radius=4),
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=10)
            )

            # Display the RGB values on the screen for reference
            cv2.putText(img, f"RGB: ({red}, {green}, {blue})", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the video frame
    cv2.imshow("CamOutput", img)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
videoCap.release()
cv2.destroyAllWindows()
ser.close()
