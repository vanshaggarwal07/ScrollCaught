# 🎮 ScrollCaught - Skyrim Skeleton Intervention

> **A computer vision productivity tool that detects doomscrolling and plays the iconic Skyrim Skeleton to get you back on track.**

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

**ScrollCaught** is an innovative productivity tool that uses your webcam and real-time face detection to monitor your attention patterns. When it detects you're doomscrolling on your phone instead of focusing on work, it playfully interrupts you with the legendary Skyrim Skeleton video.

Inspired by the viral **Skeleton** trend on TikTok, this tool combines **MediaPipe face mesh detection** with **iris tracking** to identify downward gaze patterns that indicate phone usage, making productivity fun and engaging.

---

## ✨ Features

- 🎥 **Real-time Face & Iris Detection** - Uses MediaPipe for accurate facial landmark tracking
- 📱 **Doomscroll Detection** - Analyzes eye gaze patterns to detect phone usage
- ⏱️ **Smart Thresholds** - Configurable timers and detection sensitivity
- 🎬 **Skyrim Skeleton Intervention** - Plays the iconic Skyrim Skeleton video when doomscrolling is detected
- 🔔 **Visual Warnings** - On-screen warnings before intervention triggers
- 💻 **Cross-Platform Support** - Works on Windows, macOS, and Linux

---

## 🔧 How It Works

1. **Webcam Capture** - Continuously captures video feed from your webcam
2. **Face Detection** - Uses MediaPipe FaceLandmarker to detect facial landmarks in real-time
3. **Iris Tracking** - Analyzes iris position (landmarks 145, 159, 374, 386) to determine gaze direction
4. **Pattern Analysis** - Detects sustained downward gaze patterns indicating phone usage
5. **Intervention** - When doomscrolling threshold is exceeded, plays the Skyrim Skeleton video
6. **Visual Feedback** - Displays "LOCK IN TWIN" warning message on your screen

**Detection Logic:**
- **Thresholds** (configurable):
  - `looking_down_threshold`: 0.25 (iris position threshold)
  - `debounce_threshold`: 0.45 (for noise reduction)
  - `timer`: 2.0 seconds (before intervention triggers)

---

## 💻 System Requirements

| Requirement | Details |
|---|---|
| **Operating System** | Windows, macOS (Intel/Apple Silicon), or Linux |
| **Python Version** | 3.9 - 3.12 (NOT compatible with Python 3.13) |
| **Hardware** | Webcam/built-in camera required |
| **Permissions** | Camera access must be granted to terminal/application |
| **RAM** | Minimum 2GB recommended |
| **Processor** | Dual-core processor recommended |

---

## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/vanshaggarwal07/ScrollCaught
cd scrollcaught
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download Face Detection Model
The script will automatically download the MediaPipe FaceLandmarker model:
```bash
python download_model.py
```

This creates the `assets/face_landmarker.task` file needed for face detection.

### Step 5: Run ScrollCaught
```bash
python main.py
```

---

## 📖 Usage

### Basic Usage
```bash
python main.py
```

The application will:
1. Open your webcam feed
2. Begin monitoring for doomscrolling patterns
3. Display a real-time video feed with face detection overlays
4. Show warnings when doomscrolling is detected
5. Play the Skyrim Skeleton video when threshold is exceeded

### Controls
- **Q** - Quit the application
- **ESC** - Quit the application

---

## ⚙️ Configuration

You can customize behavior by editing configuration values in `main.py`:

### `timer`
The minimum amount of time you must be "looking down" before triggering the intervention (grace period).
- **Lower values** → Triggers faster (e.g., 1.0 seconds)
- **Higher values** → Longer grace period (e.g., 5.0 seconds)

```python
timer = 2.0  # Default: 2.0 seconds
```

### `looking_down_threshold`
The iris position threshold required to consider you as looking down.
- **Lower values** → More strict, requires stronger downward gaze (e.g., 0.15)
- **Higher values** → More sensitive, triggers on slight downward gaze (e.g., 0.35)

```python
looking_down_threshold = 0.25  # Default: 0.25
```

### `debounce_threshold`
The threshold required to exit the "looking down" state and reset.
- **Lower values** → Video stops more easily, resets faster (e.g., 0.35)
- **Higher values** → Video persists longer, more forgiving (e.g., 0.55)

```python
debounce_threshold = 0.45  # Default: 0.45
```

---

## 🛠️ Troubleshooting

### Issue: "Could not open webcam"
- Verify camera permissions in system settings
- Ensure no other application is using the camera
- Try a different camera index in the code

### Issue: Face detection not working
- Ensure good lighting conditions
- Position your face directly at the camera
- Verify `assets/face_landmarker.task` exists and is downloaded

### Issue: Doomscroll detection too sensitive
- Increase `timer` value (e.g., 5.0 seconds)
- Increase `looking_down_threshold` (e.g., 0.35)

### Issue: Doomscroll detection not sensitive enough
- Decrease `timer` value (e.g., 1.0 second)
- Decrease `looking_down_threshold` (e.g., 0.15)

### Issue: "Model file not found"
- Run `python download_model.py` to download the required model

---

## 📦 Dependencies

- **opencv-python** (4.9.0.80) - Computer vision library for webcam capture and video processing
- **mediapipe** (≥0.10.14) - Face detection and iris tracking

---

## 📁 Project Structure

```
scrollcaught/
├── main.py                      # Main application logic
├── download_model.py            # MediaPipe model downloader
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── assets/
    ├── face_landmarker.task     # MediaPipe face detection model
    └── skyrim-skeleton.mp4      # Skyrim Skeleton video (required)
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ⚠️ Important Notes

- **Privacy** - This tool runs entirely locally. No data is sent to external servers
- **Camera** - Requires active webcam access while running
- **Performance** - Works best with 30+ FPS webcam and modern processor
- **Limitations**:
  - Does not distinguish between legitimate downward gaze (reading, writing) and doomscrolling
  - Requires clear view of face and eyes for accurate detection
  - May need calibration for different lighting conditions
  - Requires `skyrim-skeleton.mp4` video file in assets folder

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- Inspired by the viral **Skyrim Skeleton** TikTok trend
- Built with [MediaPipe](https://mediapipe.dev/) for face detection
- Uses [OpenCV](https://opencv.org/) for computer vision processing

---

## 📧 Support

For bugs, feature requests, or questions:
- Open an Issue on GitHub
- Check existing discussions and documentation

---

**Lock in and stay focused! May your scrolling be prevented.** ⚔️
