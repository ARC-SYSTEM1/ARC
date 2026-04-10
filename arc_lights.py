import requests
import time

API_KEY = "0d00d91d-700a-4816-9f8c-fdbfcb7809ba"
DEVICE = "19:75:98:17:3C:DE:8F:02"
MODEL = "H6008"

URL = "https://developer-api.govee.com/v1/devices/control"
HEADERS = {
    "Govee-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def send_command(cmd_name, cmd_value, pause=2.0):
    payload = {
        "device": DEVICE,
        "model": MODEL,
        "cmd": {
            "name": cmd_name,
            "value": cmd_value
        }
    }
    try:
        r = requests.put(URL, headers=HEADERS, json=payload, timeout=10)
        print(cmd_name, cmd_value, r.status_code, r.text)
    except Exception as e:
        print("GOVEE ERROR:", e)
    time.sleep(pause)

def lights_on():
    send_command("turn", "on")
    send_command("colorTem", 3500)
    send_command("brightness", 100)

def activity_light():
    send_command("turn", "on")
    send_command("brightness", 100)
    send_command("color", {"r": 0, "g": 0, "b": 255})

def energy_flash():
    send_command("turn", "on")
    send_command("brightness", 100)
    send_command("color", {"r": 255, "g": 0, "b": 0})

def lights_off():
    send_command("brightness", 1)
    send_command("turn", "off")
    send_command("turn", "off")

def low_energy():
    print("[ARC LIGHT] LOW ENERGY")
    send_command("turn", "on")
    send_command("brightness", 30)  # dim
    send_command("colorTem", 4000)  # softer warm

def high_energy():
    print("[ARC LIGHT] HIGH ENERGY")
    send_command("turn", "on")
    send_command("brightness", 100)  # full bright
    send_command("colorTem", 3500)  # sharper white
