import requests
import speech_recognition as sr
import pyttsx3

ARC_SERVER = "http://104.196.137.79:8000"  # your live ARC server

recognizer = sr.Recognizer()
tts = pyttsx3.init()


def speak(text: str):
    print(f"ARC: {text}")
    tts.say(text)
    tts.runAndWait()


def listen() -> str | None:
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text
    except sr.UnknownValueError:
        return None
    except Exception as e:
        print("Speech error:", e)
        return None


def get_arc_state():
    try:
        r = requests.get(f"{ARC_SERVER}/state", timeout=5)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def trigger_endpoint(path: str, method: str = "get", payload: dict | None = None):
    try:
        url = f"{ARC_SERVER}{path}"
        if method == "post":
            r = requests.post(url, json=payload, timeout=5)
        else:
            r = requests.get(url, timeout=5)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def arc_command_router(text: str) -> str:
    t = text.lower()

    if "what mode" in t or "mode are we in" in t or "current mode" in t:
        state = get_arc_state()
        mode = state.get("mode", "unknown")
        energy = state.get("energy", "unknown")
        activity = state.get("activity", "unknown")
        return f"We are currently in {mode} mode. Energy is {energy}. Activity is {activity}."

    if "arrival" in t:
        trigger_endpoint("/arrival")
        return "Arrival mode activated."

    if "boost energy" in t or "energy boost" in t or "increase energy" in t:
        trigger_endpoint("/energy")
        return "Energy boost triggered."

    if "activity" in t and "increase" in t:
        trigger_endpoint("/activity")
        return "Activity triggered."

    if "standby" in t:
        trigger_endpoint("/standby")
        return "System entering standby."

    if "challenge" in t:
        trigger_endpoint("/venue_moment", method="post", payload={"moment": "challenge"})
        return "Challenge moment triggered."

    if "celebration" in t:
        trigger_endpoint("/venue_moment", method="post", payload={"moment": "celebration"})
        return "Celebration moment triggered."

    if "reset" in t:
        trigger_endpoint("/venue_moment", method="post", payload={"moment": "reset"})
        return "Reset moment triggered."

    if "finale" in t:
        trigger_endpoint("/venue_moment", method="post", payload={"moment": "finale"})
        return "Finale moment triggered."

    if "summarize tonight" in t or "summary tonight" in t:
        result = trigger_endpoint("/night_intelligence")
        return f"Tonight summary: {result}"

    return "Command not recognized."


def run_arc_voice():
    speak("ARC voice operator online.")

    while True:
        command = listen()

        if not command:
            speak("I did not catch that.")
            continue

        if command.lower() in ["exit", "quit", "stop listening"]:
            speak("ARC voice operator offline.")
            break

        response = arc_command_router(command)
        speak(response)


if __name__ == "__main__":
    run_arc_voice()
