# 🎥 Motion Detection Security System

> A real-time motion detection system that monitors your webcam and sends email alerts when motion is detected.



---

## ✨ Features

- 🎯 **Real-time Motion Detection** - Uses frame differencing algorithm for fast, efficient detection
- 📧 **Email Alerts** - Instant Gmail notifications when motion is detected
- 🎨 **Visual Feedback** - Live camera feed with bounding boxes around detected motion
- ⚙️ **Configurable Sensitivity** - Adjustable thresholds for different lighting conditions
- 📸 **Screenshot Capture** - Save snapshots of detected motion with a single keystroke
- 🔒 **Secure Credentials** - Environment-based configuration for safe credential management
- 📊 **Motion Tracking** - Displays object count and timestamp for each detection
- ⏱️ **Smart Notifications** - Cooldown period prevents email spam
- 🖥️ **Cross-Platform** - Works on macOS, Windows, and Linux

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Webcam/Camera
- Gmail account with App Password enabled

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/motion-detection-security.git
   cd motion-detection-security
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Mac/Linux
   # OR
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up credentials**
   ```bash
   cp .env.example .env
   # Edit .env with your Gmail credentials
   ```

5. **Run the application**
   ```bash
   python motion_detector.py
   ```

---

## 📋 Configuration

### Environment Variables (`.env`)

```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=xxxx xxxx xxxx xxxx
RECEIVER_EMAIL=your_email@gmail.com
```

### Sensitivity Settings

Edit these values in `motion_detector.py` to adjust detection:

```python
MOTION_THRESHOLD = 25          # Lower = more sensitive (15-50)
MIN_CONTOUR_AREA = 500         # Minimum pixels to detect as motion
NOTIFICATION_DELAY = 60        # Seconds between email alerts
```

**Tuning Guide:**
- **Too many false positives?** → Increase `MOTION_THRESHOLD` or `MIN_CONTOUR_AREA`
- **Missing real motion?** → Decrease `MOTION_THRESHOLD` or `MIN_CONTOUR_AREA`
- **Too many emails?** → Increase `NOTIFICATION_DELAY`

---

## 🎮 Usage

### Controls

| Key | Action |
|-----|--------|
| **q** | Quit the application |
| **s** | Save screenshot of current frame |

### Display Windows

- **Security Feed** - Live camera with motion detection boxes and timestamps
- **Motion Detection** - Binary threshold image showing detected areas in white

### Example Output

```
✓ Camera opened successfully
✓ Motion detection started
==============================================================
Controls:
  - Press 'q' to quit
  - Press 's' to save a snapshot
==============================================================
[2024-01-15 14:32:45] Alert sent! Motion with 2 object(s) detected.
```

---

## 🔐 Security

### Important Security Practices

✅ **Do:**
- Use `.env` file for all credentials (excluded from Git)
- Use Gmail App Passwords, not your main password
- Enable 2-Step Verification on your Gmail account
- Review `.gitignore` before committing

❌ **Don't:**
- Hardcode credentials in Python files
- Share your `.env` file
- Use regular Gmail password
- Commit `.env` to version control

### How to Get Gmail App Password

1. Go to https://myaccount.google.com/
2. Click **Security** in the left menu
3. Enable **2-Step Verification** (if not enabled)
4. Scroll to **App passwords**
5. Select **Mail** and your device type
6. Copy the generated 16-character password

---

## 📁 Project Structure

```
motion-detection-security/
├── motion_detector.py          # Main application
├── requirements.txt            # Python dependencies
├── .env.example               # Template for environment variables
├── .env                       # Your credentials (ignored by Git)
├── .gitignore                 # Git exclusion rules
├── README.md                  # This file
├── VS_CODE_SETUP.md           # VS Code setup guide
├── HOW_TO_CREATE_ENV_FILE.md  # .env file creation guide
└── snapshot_*.jpg             # Captured screenshots
```

---

## 🛠️ Technical Details

### Algorithm

The motion detection uses **frame differencing**:

1. **Convert frames to grayscale** - Reduces processing complexity
2. **Apply Gaussian blur** - Reduces noise and minor variations
3. **Calculate absolute difference** - Compares consecutive frames
4. **Apply threshold** - Converts to binary image (black/white)
5. **Dilate image** - Fills gaps and connects nearby regions
6. **Find contours** - Identifies connected components
7. **Filter by area** - Removes noise below minimum threshold

### Dependencies

- **opencv-python** (4.8.1.78) - Computer vision library
- **numpy** (1.24.3) - Numerical computing
- **python-dotenv** (1.0.0) - Environment variable management

---

## 🚨 Troubleshooting

### Camera Issues

**Error: "Could not open video stream"**
- Check camera permissions (macOS: System Preferences → Security & Privacy → Camera)
- Try different camera index: `CAMERA_URL = 1` or `2`

**No video display**
- Ensure camera has permission in system settings
- Try running with administrator privileges

### Email Issues

**Error: "SMTP Authentication Failed"**
- Verify App Password is correct (not regular Gmail password)
- Ensure 2-Step Verification is enabled
- Check email address is spelled correctly

**Emails not received**
- Verify RECEIVER_EMAIL in `.env`
- Check spam/promotions folder
- Increase `NOTIFICATION_DELAY` to test

### Python Issues

**Error: "No module named 'cv2'"**
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

**Error: "Could not find .env file"**
- Rename `.env.example` to `.env`
- Place it in the same directory as `motion_detector.py`

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Detection Speed | ~30 FPS (depends on resolution) |
| CPU Usage | Low (5-15% typical) |
| Memory Usage | ~100-150 MB |
| Email Notification Latency | 2-5 seconds |

---

## 🔧 Advanced Usage

### Run in Background (macOS/Linux)

```bash
nohup python motion_detector.py > motion_detector.log 2>&1 &
```

### Run on Startup (macOS)

Create a LaunchAgent at `~/Library/LaunchAgents/com.motion.detector.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.motion.detector</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/motion_detector.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

Then load it:
```bash
launchctl load ~/Library/LaunchAgents/com.motion.detector.plist
```

---

## 📊 Use Cases

- 🏠 **Home Security** - Monitor entry points and detect intruders
- 🏢 **Office Surveillance** - Track after-hours activity
- 🚪 **Room Monitoring** - Know when someone enters a space
- 🐾 **Pet Detection** - Monitor pet movement
- 📹 **Parking Lot Monitoring** - Detect vehicles and people
- 🏗️ **Construction Sites** - Monitor activity in restricted areas



## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙋 Support

- 📖 Check [README.md](README.md) for detailed documentation







## ⭐ Show Your Support

If you found this project helpful, please consider giving it a star! ⭐

]
**Made with ❤️ for security-conscious developers**# security-system
