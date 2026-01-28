import urllib.request
import os

url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
output_path = "assets/face_landmarker.task"

if not os.path.exists("assets"):
    os.makedirs("assets")

print(f"Downloading {url} to {output_path}...")
urllib.request.urlretrieve(url, output_path)
print("Download complete.")
