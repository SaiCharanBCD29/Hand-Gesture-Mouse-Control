import cv2
import mediapipe as mp
import pyautogui

# Initialize Mediapipe hands
hands = mp.solutions.hands.Hands(max_num_hands=1)
drawing_utils = mp.solutions.drawing_utils

# Screen size
screen_width, screen_height = pyautogui.size()

# Start webcam
camera = cv2.VideoCapture(0)

x1 = y1 = x2 = y2 = 0

while True:
    ret, image = camera.read()
    if not ret:
        break

    image = cv2.flip(image, 1)  # Mirror effect
    image_height, image_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process hand landmarks
    output_hands = hands.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks

    if all_hands:
        for hand in all_hands:
            # Draw landmarks
            drawing_utils.draw_landmarks(image, hand)

            # Extract hand landmarks
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)

                # Index finger tip
                if id == 8:
                    mouse_x = int(screen_width / image_width * x)
                    mouse_y = int(screen_height / image_height * y)
                    cv2.circle(image, (x, y), 10, (0, 255, 255), cv2.FILLED)
                    pyautogui.moveTo(mouse_x, mouse_y)
                    x1, y1 = x, y

                # Thumb tip
                if id == 4:
                    x2, y2 = x, y
                    cv2.circle(image, (x, y), 10, (0, 255, 255), cv2.FILLED)

        # Check distance between thumb and index
        dist = abs(y2 - y1)
        print("Distance:", dist)

        if dist < 40:
            pyautogui.click()
            print("Clicked")

    cv2.imshow("Hand movement video capture", image)

    key = cv2.waitKey(1)
    if key == 27:  # ESC to exit
        break

camera.release()
cv2.destroyAllWindows()