def environment_action(environment_payload):

    lights = environment_payload.get("lights")
    music = environment_payload.get("music")
    screens = environment_payload.get("screens")

    return {
        "lights_command": f"lights:{lights}",
        "music_command": f"music:{music}",
        "screens_command": f"screens:{screens}",
        "controller_status": "executed"
    }
