from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from arc_lights import lights_on
from arc_roi import ARCROIEngine

roi_engine = ARCROIEngine()

import json
import os
import time

app = FastAPI()

STATE_FILE = "/home/chadj0085/ARC/arc_state.json"
MEMORY_FILE = "/home/chadj0085/ARC/arc_memory.json"


# -------------------------
# HELPERS
# -------------------------

def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return default


def get_state():
    return load_json(
        STATE_FILE,
        {"mode": "STANDBY", "presence": 0, "activity": 0, "energy": 0}
    )


def get_memory():
    return load_json(
        MEMORY_FILE,
        {
            "current_mode": None,
            "mode_step": 0,
            "last_action_time": 0,
            "last_action": None
        }
    )


# -------------------------
# ACTION ROUTES (keep simple)
# -------------------------

@app.get("/")
def root():
    return {"status": "ARC running"}


@app.get("/state")
def state():
    return get_state()

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


@app.api_route("/arrival", methods=["GET", "POST"])
def arrival():
    state = get_state()
    state["presence"] = 1
    state["activity"] += 1
    save_state(state)

    try:
        from arc_lights import lights_on

        print("[ARC] ARRIVAL detected → turning lights ON")
        lights_on()

    except Exception as e:
        print("Arrival light trigger failed:", e)

    return {"status": "ok", "activity": state["activity"]}


from fastapi import Query

@app.api_route("/force_energy", methods=["GET", "POST"])
def force_energy(energy: int = Query(None, ge=0, le=10)):
    """
    Manually override the ARC energy level.
    If no value is provided, energy increases by 2.
    Accepts values between 0 and 10.
    """
    state = get_state()

    # Set energy manually if provided
    if energy is not None:
        state["energy"] = energy
    else:
        state["energy"] = min(state.get("energy", 0) + 2, 10)

    save_state(state)

    try:
        from arc_lights import lights_on, lights_off

        print(f"[ARC DEBUG] energy = {state['energy']}")

        if state["energy"] <= 5:
            print("[ARC DEBUG] LOW -> lights_on()")
            lights_on()
        else:
            print("[ARC DEBUG] HIGH -> lights_off()")
            lights_off()

    except Exception as e:
        print("Light trigger failed:", e)

    return {
        "status": "ok",
        "energy": state["energy"]
    }

# ===============================
# ARC ROI ENDPOINTS
# ===============================

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RevenueEntry(BaseModel):
    service: str
    amount: float
    payment_method: str
    customer_count: int = 1
    location: str = "barbershop"
    zone: str = "default"
    notes: Optional[str] = ""


@app.post("/revenue")
def log_revenue(entry: RevenueEntry):
    # Update ROI Engine
    roi_engine.log_revenue(entry.amount)
    roi_engine.log_guest(entry.customer_count)

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "service": entry.service,
        "amount": entry.amount,
        "payment_method": entry.payment_method.lower(),
        "customer_count": entry.customer_count,
        "location": entry.location,
        "zone": entry.zone,
        "notes": entry.notes,
    }

    return {
        "status": "success",
        "message": "Revenue logged successfully",
        "data": record
    }


@app.post("/guest")
def log_guest(count: int = 1):
    roi_engine.log_guest(count)
    return {
        "status": "success",
        "guests_added": count
    }


@app.get("/roi")
def get_roi():
    return roi_engine.roi_report()

from datetime import datetime

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "system": "ARC",
        "version": "1.0",
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================
# DECISION ENGINE (UI SIDE) WITH ACTION TRIGGERS
# ============================================================

def execute_action_trigger(state):
    """
    Executes ARC action triggers based on system state.
    These triggers simulate real-world interventions and
    log them into the ROI engine.
    """
    energy = state.get("energy", 0)
    presence = state.get("presence", 0)
    activity = state.get("activity", 0)

    trigger_result = "No action required"

    try:
        # ENERGY BOOST TRIGGER
        if presence > 0 and energy <= 2:
            print("[ARC TRIGGER] Energy Boost Activated")
            lights_on()
            roi_engine.log_intervention("energy_boost")
            trigger_result = "Energy Boost Activated"

        # MOMENTUM BUILD TRIGGER
        elif presence > 0 and 3 <= energy <= 5:
            print("[ARC TRIGGER] Momentum Build Triggered")
            roi_engine.log_intervention("momentum_build")
            trigger_result = "Momentum Build Triggered"

        # DEAD ZONE TRIGGER
        elif presence > 0 and activity == 0:
            print("[ARC TRIGGER] Dead Zone Intervention")
            roi_engine.log_intervention("dead_zone")
            trigger_result = "Dead Zone Intervention"

        # MAINTAIN MOMENTUM
        elif energy >= 6:
            print("[ARC TRIGGER] Maintaining Momentum")
            trigger_result = "Maintaining Momentum"

    except Exception as e:
        print("[ARC ERROR] Trigger execution failed:", e)
        trigger_result = "Trigger execution error"

    return trigger_result


def analyze(state):
    """
    Determines ARC intelligence recommendations
    and executes action triggers.
    """
    presence = state.get("presence", 0)
    activity = state.get("activity", 0)
    energy = state.get("energy", 0)
    mode = state.get("mode", "ACTIVE")

    # Execute real-time trigger logic
    trigger_status = execute_action_trigger(state)

    if energy <= 2:
        action_now = "Boost Energy"
        reason = "Energy is low"
        secondary = "Start arena moment"
        priority = "HIGH"
        mode_color = "#ff5c5c"

    elif energy <= 5:
        action_now = "Build Momentum"
        reason = "Energy is rising"
        secondary = "Boost energy"
        priority = "MEDIUM"
        mode_color = "#f0c94d"

    else:
        action_now = "Maintain Momentum"
        reason = "Energy is strong"
        secondary = "None"
        priority = "LOW"
        mode_color = "#63d471"

    return {
        "presence": presence,
        "activity": activity,
        "energy": energy,
        "mode": mode,
        "action_now": action_now,
        "reason": reason,
        "secondary": secondary,
        "priority": priority,
        "mode_color": mode_color,
        "trigger_status": trigger_status
    }


# ================================
# ARC OPERATOR DASHBOARD
# ================================
from fastapi.responses import HTMLResponse

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    state = get_state()
    roi = roi_engine.roi_report()

    presence = state.get("presence", 0)
    activity = state.get("activity", 0)
    energy = state.get("energy", 0)
    mode = state.get("mode", "ACTIVE")

    # ARC Decision Logic
    if energy <= 2:
        action_now = "Boost Energy"
        reason = "Energy is low"
        secondary = "Start arena moment"
        priority = "HIGH"
        mode_color = "#ff5c5c"
    elif energy <= 5:
        action_now = "Build Momentum"
        reason = "Energy is rising"
        secondary = "Boost energy"
        priority = "MEDIUM"
        mode_color = "#f0c94d"
    else:
        action_now = "Maintain Momentum"
        reason = "Energy is strong"
        secondary = "None"
        priority = "LOW"
        mode_color = "#63d471"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ARC Operator Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="5">
        <style>
            body {{
                margin: 0;
                padding: 20px;
                background: #0a0f18;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
            }}
            .container {{
                max-width: 900px;
                margin: auto;
            }}
            .card {{
                background: #111827;
                padding: 20px;
                margin-top: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            }}
            h1 {{
                font-size: 42px;
                margin-bottom: 10px;
            }}
            h2 {{
                color: #00ffcc;
            }}
            .metric {{
                font-size: 22px;
                margin: 10px 0;
            }}
            .status {{
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
                display: inline-block;
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }}
            .box {{
                background: #1f2937;
                padding: 15px;
                border-radius: 10px;
            }}
            @media (max-width: 600px) {{
                h1 {{
                    font-size: 28px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ARC Operator Dashboard</h1>
            <p>Arena. Rhythm. Culture.</p>

            <div class="card">
                <h2>System Status</h2>
                <div class="metric"><strong>Mode:</strong> {mode}</div>
                <div class="metric"><strong>Presence:</strong> {presence}</div>
                <div class="metric"><strong>Activity:</strong> {activity}</div>
                <div class="metric"><strong>Energy:</strong> {energy}</div>
            </div>

            <div class="card">
                <h2>ARC Intelligence</h2>
                <div class="status" style="background:{mode_color};">
                    {action_now}
                </div>
                <p><strong>Reason:</strong> {reason}</p>
                <p><strong>Secondary Action:</strong> {secondary}</p>
                <p><strong>Priority:</strong> {priority}</p>
            </div>

            <div class="card">
                <h2>ROI Intelligence</h2>
                <div class="grid">
                    <div class="box">
                        <h3>Total Revenue</h3>
                        <p>${roi.get("total_revenue", 0)}</p>
                    </div>
                    <div class="box">
                        <h3>Guest Count</h3>
                        <p>{roi.get("guest_count", 0)}</p>
                    </div>
                    <div class="box">
                        <h3>Revenue per Guest</h3>
                        <p>${roi.get("revenue_per_guest", 0)}</p>
                    </div>
                    <div class="box">
                        <h3>Revenue per Hour</h3>
                        <p>${roi.get("revenue_per_hour", 0)}</p>
                    </div>
                    <div class="box">
                        <h3>Interventions</h3>
                        <p>{roi.get("interventions", 0)}</p>
                    </div>
                    <div class="box">
                        <h3>Last Updated</h3>
                        <p>{roi.get("timestamp", "N/A")}</p>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>ARC Live Endpoints</h2>
                <p>/arrival</p>
                <p>/force_energy</p>
                <p>/revenue</p>
                <p>/guest</p>
                <p>/roi</p>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html)
