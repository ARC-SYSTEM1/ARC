import requests
from arc_voice_brain import run_arc_brain

ARC_SERVER = "http://127.0.0.1:8000"

def route_command(text):

    command = text.lower()

    if "arena mode" in command:
        try:
            requests.post(f"{ARC_SERVER}/arena/start")
            return "Arena mode started."
        except:
            return "Unable to start arena mode."

    if "standby" in command:
        try:
            requests.post(f"{ARC_SERVER}/force_standby")
            return "System entering standby."
        except:
            return "Unable to enter standby."

    if "energy" in command:
        return run_arc_brain("how is the room energy right now")

    if "room" in command:
        return run_arc_brain("how is the room doing")

    return run_arc_brain(text)
