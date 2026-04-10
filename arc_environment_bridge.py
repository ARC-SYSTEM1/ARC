def trigger_environment_sequence(action_name: str):
    action_name = action_name.lower().strip()

    print(f"[ARC ENV] Triggered: {action_name}")

    if action_name == "runner":
        print("Runner dispatched")
        return {"status": "runner"}

    if action_name == "boost":
        print("Boosting energy")
        return {"status": "boost"}

    if action_name == "arena":
        print("Arena moment started")
        return {"status": "arena"}

    if action_name == "reset":
        print("Venue reset")
        return {"status": "reset"}

    print("Unknown action")
    return {"status": "unknown"}
