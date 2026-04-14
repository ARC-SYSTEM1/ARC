# ARC API Reference
## Arena. Rhythm. Culture.

### Base URL
http://104.196.137.79:8000

Swagger Documentation:
http://104.196.137.79:8000/docs

Operator Dashboard:
http://104.196.137.79:8000/dashboard

Health Check:
http://104.196.137.79:8000/health

---

### Core System Endpoints

#### GET /
Returns the root confirmation message.

#### GET /health
Checks system health.
Response:
{
  "status": "healthy"
}

#### GET /state
Retrieves the current ARC system state.

#### POST /arrival
Triggers Arrival Mode.

#### POST /standby
Sets the system to Standby Mode.

#### POST /force_energy
Manually increases system energy.

#### POST /lights/on
Turns lights on.

#### POST /lights/off
Turns lights off.

#### POST /revenue
Logs revenue data.

#### POST /guest
Logs guest count.

#### GET /roi
Returns ROI intelligence metrics.

#### GET /dashboard
Opens the ARC Operator Dashboard.
