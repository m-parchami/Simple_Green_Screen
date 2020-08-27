
import cv2
import numpy as np

cap = cv2.VideoCapture(0)  # If you have an additional webcam you may change this line
buffer = []
background =  None
threshold = 70
mode = "capture"
while True:
    ok, frame = cap.read()
    if not ok:
        print("Capture Ended!")
        break
    cv2.imshow("camera", frame)
    key = cv2.waitKey(1) & 0xFF  # You may change this line if you need a specific FPS
    if key == ord('b'):
        if mode == "background":  # If it was taking background till now:

            # Compute background and go to capture mode
            background = np.median(buffer, axis=0)

            # In case you used other methods resulting in floating point pixels:
            background = np.asarray(background, dtype=np.uint8)

            # Background is done, go to the capture (normal) mode
            mode = "capture"

        else:
            # Free the buffer for new background computation
            buffer = []

            # Switch the mode
            mode = "background"

    elif key == ord('q'):  # Just for ending the cycle

        break

    if mode == "background":
        buffer.append(frame)

    if background is not None:  # We have a background computed
        # This is just for you to check the computed background, comment these in later usages.
        cv2.imshow("background", background)
        cv2.waitKey(1)

        sub_image = cv2.absdiff(frame, background)
        sub_image = np.sum(sub_image, axis=2)

        binary = np.zeros(sub_image.shape, dtype=np.uint8)
        binary[sub_image > threshold] = 1

        kernel = np.ones((5, 5), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((17, 17), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        masked_frame = frame.copy()
        masked_frame[binary == 0] = 0
        cv2.imshow("masked", masked_frame)  # This is the final output
        cv2.waitKey(1)