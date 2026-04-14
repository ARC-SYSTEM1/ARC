# ARC API Reference
## Arena. Rhythm. Culture.

### Base URL
http://104.196.137.79:8000

---

### System Endpoints

#### GET /
Returns the root endpoint.
- **Response:** System confirmation message.

#### GET /health
Checks system health.
- **Response:**
```json
{
  "status": "healthy"
}
