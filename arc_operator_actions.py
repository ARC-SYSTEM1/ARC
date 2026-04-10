from arc_environment_bridge import trigger_environment_sequence

_last_action = "None"


def _set_last(action):
    global _last_action
    _last_action = action


def get_last_action():
    return _last_action


def trigger_runner():
    _set_last("Runner triggered")
    return trigger_environment_sequence("runner")


def boost_energy():
    _set_last("Energy boosted")
    return trigger_environment_sequence("boost")


def start_arena_moment():
    _set_last("Arena moment started")
    return trigger_environment_sequence("arena")


def reset_venue():
    _set_last("Venue reset (standby)")
    return trigger_environment_sequence("reset")
