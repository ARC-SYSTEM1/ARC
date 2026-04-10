from arc_zone_engine import get_zones
from arc_logger import log_event

def get_zone_rebalance():
    zones = get_zones()

    if not isinstance(zones, dict) or not zones:
        return {
            "status": "no_zone_data",
            "action": "maintain",
            "reason": "no zones available",
            "strongest_zone": None,
            "weakest_zone": None
        }

    energy_map = {}
    for zone_name, zone_data in zones.items():
        if isinstance(zone_data, dict):
            energy_map[zone_name] = zone_data.get("energy", 0)
        else:
            energy_map[zone_name] = 0

    if not energy_map:
        return {
            "status": "no_zone_data",
            "action": "maintain",
            "reason": "empty energy map",
            "strongest_zone": None,
            "weakest_zone": None
        }

    strongest_zone = max(energy_map, key=energy_map.get)
    weakest_zone = min(energy_map, key=energy_map.get)

    strongest_energy = energy_map[strongest_zone]
    weakest_energy = energy_map[weakest_zone]
    delta = strongest_energy - weakest_energy

    if delta >= 3:
        log_event("zone_rebalance", f"shift_to_{weakest_zone}")
        return {
            "status": "rebalance_needed",
            "action": "launch_zone_challenge",
            "reason": f"energy imbalance detected ({delta})",
            "strongest_zone": strongest_zone,
            "weakest_zone": weakest_zone,
            "delta": delta
        }

    log_event("zone_rebalance", "balanced")
    return {
        "status": "balanced",
        "action": "maintain",
        "reason": "zones stable",
        "strongest_zone": strongest_zone,
        "weakest_zone": weakest_zone,
        "delta": delta
    }
