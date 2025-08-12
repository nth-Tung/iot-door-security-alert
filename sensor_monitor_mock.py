import time
import random
from threading import Lock
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# import hàm lấy danh sách người nhận
from email_utils import get_all_receivers

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

def send_email_to_receivers(subject, body):
    receivers = get_all_receivers()
    if not receivers:
        print("Danh sách người nhận trống, bỏ qua gửi email.")
        return

    # Tạo kết nối SMTP
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

def log_event(event):
    with log_lock:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        event_log.append({'time': timestamp, 'event': event})
        print(f"[{timestamp}] {event}")

        send_email_to_receivers(
            "Cảnh báo an ninh cửa",
            f"{timestamp} - {event}"
        )

def short_alarm():
    sensor_status['alarm'] = True
    time.sleep(3)
    sensor_status['alarm'] = False

def monitor_sensors():
    while True:
        # Giả lập trạng thái ngẫu nhiên
        pir = random.choice([False, False, False, True])  # ít xảy ra chuyển động
        reed = random.choice([True, True, True, False])  # ít cửa mở
        button = random.choice([True, True, True, False]) # ít nhấn chuông

        sensor_status['pir'] = pir
        sensor_status['reed'] = reed
        sensor_status['button'] = button

        if pir:
            log_event("Giả lập phát hiện chuyển động!")
            short_alarm()
        if not reed:
            log_event("Giả lập cửa mở!")
            short_alarm()
        if not button:
            log_event("Giả lập chuông nhấn!")
            short_alarm()

        time.sleep(5)

def get_status():
    with log_lock:
        return sensor_status.copy(), event_log[-20:]

if __name__ == "__main__":
    monitor_sensors()
