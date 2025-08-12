from gpiozero import MotionSensor, Button, LED, Buzzer
from signal import pause
import time
from threading import Thread, Lock
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import traceback

# import hàm lấy danh sách người nhận
from email_utils import get_all_receivers

# Khai báo các chân GPIO
PIR_PIN = 17
REED_PIN = 27
BUTTON_PIN = 22
BUZZER_PIN = 18
LED_PIN = 23

# Khởi tạo thiết bị
pir = MotionSensor(PIR_PIN)
reed = Button(REED_PIN, pull_up=True)
button = Button(BUTTON_PIN, pull_up=True)
led = LED(LED_PIN)
buzzer = Buzzer(BUZZER_PIN)

sensor_status = {
    'pir': False,
    'reed': True,
    'button': True,
    'alarm': False
}

event_log = []
log_lock = Lock()

# Cấu hình email gửi
SENDER_EMAIL = 'your_email@gmail.com'
SENDER_NAME = 'Hệ thống cảnh báo cửa'
SENDER_PASSWORD = 'your_app_password'  # Mật khẩu ứng dụng Gmail

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

# Thời gian debounce gửi email (giây)
DEBOUNCE_TIME = 120
last_email_times = {
    'pir': 0,
    'reed': 0,
    'button': 0
}

def send_email_to_receivers(subject, body):
    receivers = get_all_receivers()
    if not receivers:
        print("Danh sách người nhận trống, bỏ qua gửi email.")
        return

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)

            for name, email in receivers:
                msg = MIMEMultipart()
                msg['From'] = formataddr((SENDER_NAME, SENDER_EMAIL))
                msg['To'] = email
                msg['Subject'] = subject

                body_with_greeting = f"Xin chào {name},\n\n{body}\n\nTrân trọng,\n{SENDER_NAME}"
                msg.attach(MIMEText(body_with_greeting, 'plain'))

                smtp.sendmail(SENDER_EMAIL, email, msg.as_string())
                print(f"Đã gửi email cảnh báo đến: {name} <{email}>")

    except Exception as e:
        print("Lỗi gửi email:", e)
        traceback.print_exc()

def log_event(event, event_type=None):
    global last_email_times
    with log_lock:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        event_log.append({'time': timestamp, 'event': event})
        print(f"[{timestamp}] {event}")

        # Kiểm tra debounce gửi email
        if event_type:
            now = time.time()
            if now - last_email_times.get(event_type, 0) > DEBOUNCE_TIME:
                send_email_to_receivers(
                    "Cảnh báo an ninh cửa",
                    f"{timestamp} - {event}"
                )
                last_email_times[event_type] = now
            else:
                print(f"Đã gửi email cảnh báo '{event_type}' gần đây, bỏ qua gửi lại.")

def alarm_on():
    led.on()
    buzzer.on()
    sensor_status['alarm'] = True

def alarm_off():
    led.off()
    buzzer.off()
    sensor_status['alarm'] = False

def short_alarm():
    try:
        alarm_on()
        time.sleep(3)
        alarm_off()
    except Exception:
        print("Lỗi trong thread alarm:")
        traceback.print_exc()

def on_motion():
    sensor_status['pir'] = True
    log_event("Phát hiện chuyển động!", event_type='pir')
    Thread(target=short_alarm, daemon=True).start()
    sensor_status['pir'] = False

def on_door_open():
    sensor_status['reed'] = False
    log_event("Cửa bị mở!", event_type='reed')
    Thread(target=short_alarm, daemon=True).start()
    sensor_status['reed'] = True

def on_button_press():
    sensor_status['button'] = False
    log_event("Chuông cửa được nhấn!", event_type='button')
    Thread(target=short_alarm, daemon=True).start()
    sensor_status['button'] = True

# Gán callback sự kiện
pir.when_motion = on_motion
reed.when_pressed = on_door_open
button.when_pressed = on_button_press

def get_status():
    with log_lock:
        return sensor_status.copy(), event_log[-20:]

if __name__ == "__main__":
    print("Bắt đầu giám sát cảm biến...")
    try:
        pause()  # Chạy vòng lặp chờ sự kiện
    except KeyboardInterrupt:
        print("Dừng chương trình bằng Ctrl+C")
