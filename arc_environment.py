from arc_lights import lights_on, lights_off, energy_flash
from arc_music import play_welcome, play_energy, stop_music
from arc_voice import say_arrival, say_energy, say_standby

def arrival_mode():
    lights_on()
    play_welcome()
    say_arrival()
    return {"mode": "arrival"}

def standby_mode():
    lights_off()
    stop_music()
    say_standby()
    return {"mode": "standby"}

def energy_mode():
    energy_flash()
    play_energy()
    say_energy()
    return {"mode": "energy"}
