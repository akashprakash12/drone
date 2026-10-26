# AI UNLOCKED Drone Vision Lab — corrected reporting project

## Before starting

1. Copy your existing 11 compressed model files into `assets/compressed/` (campus, five people, two vehicles, three trees). These models were not supplied with the uploaded project. The included drone model is `assets/drone_scout.glb`.
2. Keep your existing `automation_config.json` in the project root. Do not upload it to GitHub. The `setup.ps1` script can create one if it is missing.
3. Keep your original `n8n_data` volume and backup. Do not run the original `n8n-drone` container at the same time as Compose n8n.
4. Stop any older dashboard container using port 8000.
5. From PowerShell in this directory run `./setup.ps1`, then `docker compose up -d --build` and `docker compose ps`.
6. Import `n8n_reporting_workflow.json` into n8n at http://localhost:5678. In the Launch Drone HTTP Request node, replace `REPLACE_WITH_TOKEN_FROM_automation_config.json` with your token, or configure a credential instead. If you have an existing active workflow, deactivate it before activating the imported version to avoid duplicates.
7. Keep http://localhost:8000 open in a browser throughout the mission: the browser runs the simulated scan. Launch -> 75-second wait -> GET detections -> XLSX.
8. Run one execution and check `files/drone_detection_report.xlsx` in your Windows project.

## Report behavior

A complete mission scans 10 targets in approximately 61 seconds. The automation waits 75 seconds to allow the browser to finish. Each report contains the objects actually recorded by the browser (up to 10 unique objects), not fabricated detections. The same XLSX filename is overwritten each run. The `Convert to XLSX` node must use binary output field `data`.

## Verification

- `docker compose config` validates Compose.
- `Invoke-RestMethod http://localhost:8000/api/status` checks the dashboard.
- `Invoke-RestMethod http://localhost:8000/api/detections | ConvertTo-Json -Depth 10` shows the count and records.
- `Get-Item .\files\drone_detection_report.xlsx` checks the output.

If `count` is less than 10 after the mission, check the browser console, whether the page remained open, and whether model loading finished. If the API has 10 detections but the XLSX has fewer rows, inspect the Split Out and Convert to XLSX node item counts.

The demo uses scripted simulated detection, not real AI inference.
