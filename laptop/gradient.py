import cv2
import mediapipe as mp
import serial
import time

# Initialize serial communication (adjust COM port and baud rate as needed)
ser = serial.Serial('/dev/cu.usbserial-210', 9600)
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

    # Process hand landmarks
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    recHands = hands.process(img_rgb)

    # Check if a hand is detected
    if recHands.multi_hand_landmarks:
        for hand_landmarks in recHands.multi_hand_landmarks:
            # Extract the x and y coordinates of the index finger tip (landmark 8)
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            # Map x to Red (0 to 255) and y to Green/Blue (0 to 255) for gradient effect
            red = int((x / w) * 255)
            green = int((y / h) * 255)
            blue = 255 - green  # Inverse of green for a complementary gradient effect

            # Send RGB values to Arduino as a formatted string
            rgb_message = f"{red},{green},{blue}\n"  # Format: "R,G,B\n"
            ser.write(rgb_message.encode())

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
