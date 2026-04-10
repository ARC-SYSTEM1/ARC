zones = {}
def get_zones(): return zones
def get_zone(name): return zones.get(name, {})
def set_zone_presence(name, state=True):
    zones.setdefault(name, {})
    zones[name]["presence"] = state
def clear_zone_presence(name):
    zones.setdefault(name, {})
    zones[name]["presence"] = False
def add_activity(name, amount=1):
    zones.setdefault(name, {})
    zones[name]["activity"] = zones[name].get("activity", 0) + amount
def add_energy(name, amount=1):
    zones.setdefault(name, {})
    zones[name]["energy"] = zones[name].get("energy", 0) + amount
def reset_zone(name):
    zones[name] = {}
