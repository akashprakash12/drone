AI UNLOCKED — DRONE DETECTION REPORTING FIX

1. Extract ZIP; open PowerShell inside extracted folder.
2. Stop old Python server with Ctrl+C. Run: python server.py
3. Open http://localhost:8000/ and verify 3D model.
4. Open http://localhost:8000/api/detections — JSON should appear (not 404).
5. In Docker n8n, Get Detections HTTP Request: GET http://host.docker.internal:8000/api/detections
6. In n8n Launch POST, use http://host.docker.internal:8000/api/launch with header
   X-Demo-Token set to the exact value in automation_config.json (do NOT paste the placeholder).
7. Import n8n_reporting_workflow.json if preferred. Check all node parameters.
8. For XLSX saving, mount a Windows folder to /files in your Docker n8n container.
   Example docker-compose volume: C:/AI_UNLOCKED/reports:/files
9. The workflow has a 10-minute schedule interval PLUS a 10-minute Wait node.
   For ONE test 10 minutes after manual execution, use Manual Trigger -> Wait 10 min -> Launch.
   For a 10-minute recurring interval, REMOVE the 10-minute Wait.
10. Leave the dashboard browser tab open. It produces scripted detections over ~35 seconds.
11. The dashboard posts simulated detection events to Python; n8n fetches them after 40 sec.
12. Do not expose port 8000 to the internet or untrusted networks.
13. Three.js imports require internet access (jsDelivr).
14. This is NOT real camera-based AI detection.

Troubleshooting:
- 404 on /api/detections: old server.py is running; stop it and start this new one.
- 403 on /api/launch: header token does not match automation_config.json.
- 404 on /: run python server.py from the extracted folder containing index.html.
- Docker file save error: mount /files, or use Convert to File and download binary from n8n.
- No rows: keep browser open, launch mission, wait until it completes, then GET detections.
