import speech_recognition as sr
from arc_command_router import route_command


def speak(text):
    print("ARC:", text)


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("ARC listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Operator:", text)
        return text
    except:
        return None


def run():
    speak("ARC operator assistant online.")

    while True:
        command = listen()

        if not command:
            continue

        if "exit arc" in command.lower():
            speak("ARC voice operator offline.")
            break

        response = route_command(command)
        speak(response)


if __name__ == "__main__":
    run()
