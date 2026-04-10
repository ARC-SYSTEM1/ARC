import time
from arc_autopilot import run_autopilot
from arc_moment_autopilot import run_moment_autopilot
from arc_logger import log_event

INTERVAL = 8

def run_pulse_loop():
    log_event("pulse", "started")
    print("ARC Pulse Engine running...")
    while True:
        try:
            result = run_autopilot()
            action = result.get("autopilot", "unknown")
            log_event("pulse", action)
            print("pulse:", action)
        except Exception as e:
            log_event("pulse_error", str(e))
            print("pulse_error:", e)

        try:
            m_result = run_moment_autopilot()
            m_action = m_result.get("moment_autopilot", "unknown")
            log_event("pulse_moment", m_action)
            print("pulse_moment:", m_action)
        except Exception as e:
            log_event("pulse_moment_error", str(e))
            print("pulse_moment_error:", e)

        time.sleep(INTERVAL)

if __name__ == "__main__":
    run_pulse_loop()
