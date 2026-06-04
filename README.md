# YouTube Downloader (ฺBy BIOAE) 

A sleek, standalone YouTube(and some facebook & reels) video downloader app. It is cross-platform and specifically optimized to handle SSL certificate overrides on macOS and format conversions on Windows.

## 🎬 Key Features
- **Custom Sci-Fi UI:** Dark-red themed interface designed with premium custom-colored download buttons.
- **File Type Choices:** Allows users to choose their preferred output format between **MP4**, **MOV**, and **WMV**.
- **Quality Configurations:** Supports high-resolution video streams including **480P**, **720P**, **1080P (Full HD)**, and up to **4K (Ultra HD)**.
- **Custom Storage Path:** Flexible folder destination selector (Simply double-click the Path box to browse directories).
- **Mac SSL Fix Pre-built:** Bypasses macOS-specific Python `CERTIFICATE_VERIFY_FAILED` errors automatically.

---

## 🛠️ Prerequisites

Before installing the app, please ensure you have the following system dependencies installed:

1. **Python 3.x**
2. **FFmpeg** (Required for merging high-quality video/audio tracks and converting to MOV/WMV)
   - **macOS (via Homebrew):** `brew install ffmpeg`
   - **Windows:** Download the `ffmpeg.exe` binary and place it directly inside your script folder.

---

## 💻 Installation & Usage

Follow these simple terminal commands to run the script locally:

1. Clone this repository to your machine:
```bash
git clone [https://github.com/Bioae/Youtube-Downloader-app.git](https://github.com/Bioae/Youtube-Downloader-app.git)
cd Youtube-Downloader-app
