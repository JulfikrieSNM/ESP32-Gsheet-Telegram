from machine import Pin, time_pulse_us
import urequests
from time import sleep
import time

# Pin setup
TRIG_PIN = Pin(5, Pin.OUT)
ECHO_PIN = Pin(18, Pin.IN)
BUZZER_PIN = Pin(19, Pin.OUT)

# Wi-Fi Connection
def connect():
    import network
    ssid = "smartspacekk"
    password = "smartspace09"
    station = network.WLAN(network.STA_IF)

    if not station.isconnected():
        station.active(True)
        station.connect(ssid, password)
        while not station.isconnected():
            pass

    print("Connection successful")
    print(station.ifconfig())

connect()

# Telegram Bot Credentials
BOT_TOKEN = 'your_bot_token_here'
CHAT_ID = 'your_chat_id_here'

# Send message to Telegram
def send_telegram_message(distance):
    message = "🚨 Distance Detected: {:.2f} cm".format(distance)
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(
        BOT_TOKEN, CHAT_ID, message)
    try:
        response = urequests.get(url)
        response.close()
        print("Telegram message sent")
    except:
        print("Failed to send Telegram message")

# Get Distance Function
def get_distance():
    TRIG_PIN.off()
    time.sleep_us(2)
    TRIG_PIN.on()
    time.sleep_us(10)
    TRIG_PIN.off()

    duration = time_pulse_us(ECHO_PIN, 1, 30000)  # 30ms timeout
    if duration < 0:
        return -1
    distance_cm = (duration / 2) / 29.1
    return distance_cm

# Main Loop
while True:
    distance = get_distance()

    if distance > 0:
        print("Distance: {:.2f} cm".format(distance))

        if distance < 5:
            BUZZER_PIN.on()
            send_telegram_message(distance)  # Send only when object is near
        else:
            BUZZER_PIN.off()
    else:
        print("Error reading distance")

    # Send to Google Form
    h = {'content-type': 'application/x-www-form-urlencoded'}
    form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSeKT-7XwFW3nxrGBhprCks2jXZWOCj-UAm2gq1-jFEOyXSLLA/formResponse?usp=pp_url&'
    form_data = 'entry.108654085=' + str(distance)
    try:
        r = urequests.post(form_url, data=form_data, headers=h)
        r.close()
        print("Data sent to Google Form")
    except:
        print("Failed to send to Google Form")

    time.sleep(10)
