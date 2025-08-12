# Door Security Alert System (Raspberry Pi & Flask)

This project is a basic IoT-based **Door Security Alert System** using a Raspberry Pi, PIR motion sensor, reed switch, LED, buzzer, and Flask for the web interface. It detects movement or door opening, triggers visual/audible alerts, and sends email notifications to predefined recipients stored in a database.

---

## 🚀 Features

- **Motion Detection** using a PIR sensor
- **Door Open Detection** using a reed switch
- **Visual Alert** with an LED
- **Audible Alert** with a buzzer
- **Email Notification** to multiple recipients stored in a database
- **Web Interface** to view live status and history of alerts

---

## 🛠 Requirements

- Python 3.9+
- Flask
- Flask-Mail
- Flask-SQLAlchemy
- GPIO Zero (for Raspberry Pi)
- A Gmail account with **App Password** enabled

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nth-Tung/iot-door-security-alert.git
cd iot-door-security-alert
```

### 2. Install Dependencies

If running on **Windows** (development mode, without hardware):
```bash
pip install -r requirements.txt
```

If running on **Raspberry Pi** (with hardware connected):
```bash
pip install -r requirements.txt
sudo apt update
sudo apt install python3-gpiozero
```

---

## ⚙️ Email Configuration

Before running, configure the email settings in your main configuration file (e.g., `config.py` or inside your main Python script):

```python
SENDER_EMAIL = 'your_email@gmail.com'
SENDER_NAME = 'Door Security Alert System'
SENDER_PASSWORD = 'your_app_password'  # Gmail App Password
```

**Note**:
- You must use a Gmail **App Password** (not your regular password).
- To generate an App Password:
  1. Enable **2-Step Verification** on your Gmail account.
  2. Go to [Google App Passwords](https://myaccount.google.com/security).
  3. Generate a password for "Mail" and your device.

---

## ▶️ Running the Project

```bash
python app.py
```

The server will start, and you can access the web interface at:
```
http://localhost:5000
```

Or, on a Raspberry Pi's local network IP, e.g.:
```
http://192.168.1.50:5000
```

---

## 📌 Hardware Setup (Raspberry Pi)

- **PIR Sensor**: Detects motion
- **Reed Switch**: Detects door open/close
- **LED**: Provides visual alerts
- **Buzzer**: Provides audible alerts

---

## 📝 Notes

- Ensure all hardware components are properly connected to the Raspberry Pi GPIO pins as per your script's configuration.
- Replace `your-username` in the `git clone` command with your actual GitHub username.
- For production use, consider securing the Flask app with HTTPS and proper authentication.
