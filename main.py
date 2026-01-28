import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
from pathlib import Path
import sys


def play_video(skeleton_cap) -> None:
    """Prepare video for playback on Windows"""
    pass


def close_video(skeleton_cap) -> None:
    """Close video capture on Windows"""
    if skeleton_cap is not None:
        skeleton_cap.release()
        cv2.destroyWindow('Skyrim Skeleton')

def draw_warning(frame, text="lock in twin"):
    h, w = frame.shape[:2]
    box_w, box_h = 500, 70
    x1 = (w - box_w) // 2
    y1 = 24
    x2 = x1 + box_w
    y2 = y1 + box_h

    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (15, 0, 15), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)
    cv2.rectangle(frame, (x1-2, y1-2), (x2+2, y2+2), (80, 255, 160) , 4)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 255, 160) , 2)

    cv2.putText(
        frame,
        text.upper(),
        (x1 + 26, y1 + 48),
        cv2.FONT_HERSHEY_DUPLEX,
        1.2,
        (255, 255, 255),
        3,
        cv2.LINE_AA,
    )


    
def main():
    timer = 2.0
    looking_down_threshold = 0.25
    debounce_threshold = 0.45
    
    skyrim_skeleton_video = Path("./assets/skyrim-skeleton.mp4").resolve()
    if not skyrim_skeleton_video.exists():
        print("Could not open skyrim-skeleton.mp4")
        return
    
    base_options = python.BaseOptions(model_asset_path='assets/face_landmarker.task')
    options = vision.FaceLandmarkerOptions(base_options=base_options,
                                           output_face_blendshapes=False,
                                           output_facial_transformation_matrixes=False,
                                           num_faces=1)
    detector = vision.FaceLandmarker.create_from_options(options)

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Could not open webcam")
        return
    
    doomscroll = None
    video_playing = False
    skeleton_cap = None
    last_frame_time = time.time()
    frame_delay = 33  # ~30 FPS in milliseconds

    while True:
        ret, frame = cam.read()
        if not ret:
            continue
        
        frame = cv2.flip(frame, 1)
        height, width, depth = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        detection_result = detector.detect(mp_image)
        face_landmark_points = detection_result.face_landmarks

        current = time.time()

        if face_landmark_points:
            one_face_landmark_points = face_landmark_points[0]
            
            left = [one_face_landmark_points[145], one_face_landmark_points[159]]
            for landmark_point in left:
                x = int(landmark_point.x * width)
                y = int(landmark_point.y * height)

            right = [one_face_landmark_points[374], one_face_landmark_points[386]]
            for landmark_point in right:
                    x = int(landmark_point.x * width)
                    y = int(landmark_point.y * height)
                 
            
            lx = int((left[0].x + left[1].x) / 2 * width)
            ly = int((left[0].y + left[1].y) / 2 * height)

            rx = int((right[0].x + right[1].x) / 2 * width)
            ry = int((right[0].y + right[1].y) / 2 * height)

            box = 50

            cv2.rectangle(frame, (lx - box, ly - box), (lx + box, ly + box), (10, 255, 0), 2)
            cv2.rectangle(frame, (rx - box, ry - box), (rx + box, ry + box), (10, 255, 0), 2)
            

            l_iris = one_face_landmark_points[468]
            r_iris = one_face_landmark_points[473]
            
            l_ratio = (l_iris.y  - left[1].y)  / (left[0].y  - left[1].y  + 1e-6)
            r_ratio = (r_iris.y - right[1].y) / (right[0].y - right[1].y + 1e-6)

            avg_ratio = (l_ratio + r_ratio) / 2.0
            # print(f"Ratio: {avg_ratio:.3f} | Threshold: {looking_down_threshold}")

            if video_playing:
                is_looking_down = avg_ratio < debounce_threshold
            else:
                is_looking_down = avg_ratio < looking_down_threshold


            if is_looking_down:
                if doomscroll is None:
                    doomscroll = current

                if (current - doomscroll) >= timer:               
                    if not video_playing:
                        video_playing = True
                        if skeleton_cap is None:
                            skeleton_cap = cv2.VideoCapture(str(skyrim_skeleton_video))
                            if not skeleton_cap.isOpened():
                                print(f"Error: Could not open video file at {skyrim_skeleton_video}")
                                skeleton_cap = None
                                video_playing = False

            else:
                doomscroll = None
                if video_playing:
                    video_playing = False
                    if skeleton_cap is not None:
                        skeleton_cap.release()
                        cv2.destroyWindow('Skyrim Skeleton')
                        skeleton_cap = None
        else:
            doomscroll = None
            if video_playing:
                video_playing = False
                if skeleton_cap is not None:
                    skeleton_cap.release()
                    cv2.destroyWindow('Skyrim Skeleton')
                    skeleton_cap = None

        if video_playing:
            draw_warning(frame, "doomscrolling alarm")
            if skeleton_cap is not None:
                ret2, skeleton_frame = skeleton_cap.read()
                if not ret2:
                    # Loop video back to start
                    skeleton_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret2, skeleton_frame = skeleton_cap.read()
                if ret2:
                    # Resize to match window dimensions
                    skeleton_frame = cv2.resize(skeleton_frame, (390, 780))
                    cv2.imshow('Skyrim Skeleton', skeleton_frame)
                    cv2.moveWindow('Skyrim Skeleton', 25, 45)

        cv2.imshow('lock in', frame)
        key = cv2.waitKey(1)

        if key == 27:
            break

    if video_playing:
        if skeleton_cap is not None:
            skeleton_cap.release()
            cv2.destroyWindow('Skyrim Skeleton')
            skeleton_cap = None

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()


