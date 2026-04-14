# ARC CONTROL MAP
## Arena. Rhythm. Culture.

### Purpose
This document defines the operational control flow of the ARC System. It provides a clear and structured overview of how inputs are processed into decisions, actions, and measurable outcomes.

---

## 1. ARC Core Control Loop

Signals → State → Decision → Action → Outcome → ROI

This loop represents the intelligence backbone of ARC and governs all system behavior.

---

## 2. System Inputs (Signals)

| Signal | Source | Description |
|--------|--------|-------------|
| Presence | Sensors / Manual Input | Detects occupancy in the environment |
| Activity | Operator / Sensors | Measures engagement levels |
| Energy | Decision Engine | Indicates overall room momentum |
| Revenue | POS / Manual Entry | Tracks financial performance |
| Guest Count | Operator Input | Logs attendance data |
| Time | System Clock | Enables time-based automation |

---

## 3. System State

| State | Description |
|-------|-------------|
| Standby | Idle state when no presence is detected |
| Arrival | Activated when presence is detected |
| Active | Operational mode during engagement |
| Energy Boost | Elevated environment state |
| Alert | Triggered during anomalies or thresholds |
| Shutdown | System safely powers down |

---

## 4. Decision Engine Logic

| Condition | Decision |
|-----------|----------|
| Presence Detected | Trigger Arrival Mode |
| No Presence | Enter Standby Mode |
| Low Energy | Initiate Energy Boost |
| High Activity | Maintain Active Mode |
| Revenue Spike | Log Event and Adjust Metrics |
| System Idle | Optimize Resource Usage |

---

## 5. System Actions

| Action | Endpoint |
|--------|----------|
| Activate Arrival Mode | `/arrival` |
| Enter Standby Mode | `/standby` |
| Increase Energy | `/force_energy` |
| Turn Lights On | `/lights/on` |
| Turn Lights Off | `/lights/off` |
| Log Revenue | `/revenue` |
| Log Guest Count | `/guest` |
| Retrieve System State | `/state` |
| Health Check | `/health` |
| Open Dashboard | `/dashboard` |
| Retrieve ROI Metrics | `/roi` |

---

## 6. System Outputs

| Output | Description |
|--------|-------------|
| Lighting Control | Smart environment adjustments |
| Dashboard Updates | Real-time monitoring |
| Event Logs | Operational history |
| KPI and ROI Data | Performance insights |
| Automated Triggers | Intelligent system responses |

---

## 7. Data Flow Architecture

Sensors → ARC API (FastAPI) → State Engine → Decision Engine → Environment Controller → Dashboard → ROI & KPI Analytics

---

## 8. Operational Objectives

- Ensure predictable and reliable automation.
- Provide measurable operational insights.
- Support real-world validation.
- Maintain scalability and vendor neutrality.
- Enable data-driven decision-making.

---

## 9. Governance Alignment

This document supports:
- Technical Validation
- Controlled Real-World Deployment
- Risk Mitigation
- Intelligence Development
- Commercial Readiness

---

## Version Control

**Version:** v1.0.0 
**Status:** Approved – Technical Governance 
**Owner:** ARC Development 
**Last Updated:** April 2026
