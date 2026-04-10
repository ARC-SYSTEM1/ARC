AUTOPILOT_ENABLED = True
OVERRIDE_ACTIVE = False
FORCED_ACTION = None


def disable_autopilot():
    global AUTOPILOT_ENABLED
    AUTOPILOT_ENABLED = False
    return {
        "status": "autopilot_disabled"
    }


def enable_autopilot():
    global AUTOPILOT_ENABLED
    AUTOPILOT_ENABLED = True
    return {
        "status": "autopilot_enabled"
    }


def activate_override():
    global OVERRIDE_ACTIVE
    OVERRIDE_ACTIVE = True
    return {
        "status": "override_active"
    }


def deactivate_override():
    global OVERRIDE_ACTIVE
    OVERRIDE_ACTIVE = False
    return {
        "status": "override_inactive"
    }


def set_forced_action(action_name):
    global FORCED_ACTION
    FORCED_ACTION = action_name
    return {
        "status": "forced_action_set",
        "forced_action": FORCED_ACTION
    }


def clear_forced_action():
    global FORCED_ACTION
    FORCED_ACTION = None
    return {
        "status": "forced_action_cleared"
    }


def get_override_status():
    return {
        "autopilot_enabled": AUTOPILOT_ENABLED,
        "override_active": OVERRIDE_ACTIVE,
        "forced_action": FORCED_ACTION
    }
