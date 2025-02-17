import cv2
import mediapipe as mp
import pyautogui
import time

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

blink_start_time = 0
blink_duration = 0
sensitivity_factor = 1.6  

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1) 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
        
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))  
            if id == 1:
                
                screen_x = sensitivity_factor * (screen_w * landmark.x)
                screen_y = sensitivity_factor * (screen_h * landmark.y)
                
                pyautogui.moveTo(screen_x, screen_y, duration=0.05)  

                
                if landmark.y > 0.7:  
                    pyautogui.scroll(-10)
                elif landmark.y < 0.3:  
                    pyautogui.scroll(10)

        
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))  

        
        if (left[0].y - left[1].y) < 0.004:  
            if blink_start_time == 0:  
                blink_start_time = time.time()
            blink_duration = time.time() - blink_start_time

            if blink_duration > 0.5:  # If blink lasts longer than 0.5 seconds
                pyautogui.rightClick()  # Right click for long blink
                pyautogui.sleep(1)  # Pause to prevent multiple clicks
        else:
            if blink_duration < 0.5 and blink_start_time != 0:  # Short blink
                pyautogui.click()  # Left click for short blink
                pyautogui.sleep(1)
            blink_start_time = 0  # Reset blink st  art time

    # Display the frame with circles
    cv2.imshow('Eye Controlled Mouse', frame)

    # Exit mechanism
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera and close windows
cam.release()
cv2.destroyAllWindows()

