import requests
import time

ARC_URL = "http://127.0.0.1:8000"

presence_detected = False


def trigger_arrival():
    requests.post(f"{ARC_URL}/arrival", timeout=5)


def trigger_standby():
    requests.post(f"{ARC_URL}/standby", timeout=5)


def trigger_energy(level=7):
    requests.post(f"{ARC_URL}/force_energy?energy={level}", timeout=5)


def simulate_sensor():
    global presence_detected
    print("[ARC SENSOR] Aqara Simulation Bridge Started")
    print("Enter 1 for presence, 0 for no presence.\n")

    while True:
        try:
            state = input("Presence (1/0): ").strip()

            if state == "1" and not presence_detected:
                print("[ARC SENSOR] Presence detected → ARRIVAL")
                trigger_arrival()
                trigger_energy(7)
                presence_detected = True

            elif state == "0" and presence_detected:
                print("[ARC SENSOR] No presence detected → STANDBY")
                trigger_standby()
                presence_detected = False

        except Exception as e:
            print("[ARC SENSOR ERROR]", e)

        time.sleep(1)


if __name__ == "__main__":
    simulate_sensor()
