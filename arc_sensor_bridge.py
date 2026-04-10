import requests
import time

ARC_URL = "http://127.0.0.1:8000/arrival"

def send_arrival():
    try:
        response = requests.post(ARC_URL, timeout=15)
        print("[SENSOR] Arrival Triggered")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print("[SENSOR ERROR]", e)

if __name__ == "__main__":
    print("Starting ARC Sensor Bridge...")
    while True:
        send_arrival()
        time.sleep(10)
