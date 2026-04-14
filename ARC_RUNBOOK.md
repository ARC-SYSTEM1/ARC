# ARC Runbook
## Arena. Rhythm. Culture.

### Start ARC
```bash
cd ~/ARC
source ~/arc_env/bin/activate
fuser -k 8000/tcp
uvicorn arc_server:app --host 0.0.0.0 --port 8000 --reload
