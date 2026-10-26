AI UNLOCKED — DRONE OBJECT DETECTION (CLASSROOM SIMULATION)

WHAT THIS IS
A 3D drone flyover with SCRIPTED bounding boxes and confidence scores for four
campus objects (building, vehicle, tree, person). This is a teaching simulation,
NOT a real camera feed or trained object-detection AI.

WINDOWS SETUP
1. Extract ZIP fully. Keep index.html, server.py, automation_config.json,
   and assets/drone_scout.glb together in the same folder.
2. Stop your old Python server (Ctrl+C). Open PowerShell in this new folder.
3. Run: python server.py
4. Open: http://localhost:8000
5. Wait for the drone to load. Use dashboard Launch/Stop/Reset as a backup.
6. Open Docker n8n at http://localhost:5678.
7. Import n8n_launch.json, n8n_stop.json and n8n_reset.json as three workflows.
   Execute each workflow manually to trigger its corresponding command.
8. In the n8n HTTP Request node, URL should be:
   http://host.docker.internal:8000/api/launch (or /stop or /reset)
   Header X-Demo-Token must equal the value in automation_config.json.
9. If n8n says 403: update the header token and restart python server.py.
10. If n8n says 404: verify the URL uses /api/launch, /api/stop or /api/reset.
11. If n8n cannot connect: keep Python running; Docker uses host.docker.internal.
12. If the drone model is blank: verify assets/drone_scout.glb and internet
    connection (Three.js is loaded from jsDelivr CDN).

SECURITY
This bundle contains a newly generated private token. Do not post it online.
The Python server listens on port 8000 on all network interfaces to let Docker
connect. Do not expose port 8000 to the internet or untrusted Wi-Fi networks.
Use Windows Firewall to restrict access. No real drone is controlled.

TESTING
Start dashboard first, then execute n8n_launch. You should see takeoff and
four scripted detection labels. Execute n8n_stop mid-flight to freeze it.
Execute n8n_reset to return to STANDBY. If you restart the server, refresh
Chrome before sending the first n8n command.

SCHEDULING
These imported workflows are manual by design to avoid surprise launches.
To schedule one, create a Schedule Trigger and connect it to Launch Drone.
Set timezone Asia/Kolkata and publish only after testing.
