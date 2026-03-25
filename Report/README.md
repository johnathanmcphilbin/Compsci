# Artefact Technical Guide

This folder contains the essential digital components of the Environmental Monitoring & Flood Risk System.

## Folder Structure

- **`forest_model/`**: Contains the core Python risk model (`model.py`) and calculated results (`results.json`).
- **`data/`**: Contains all environmental datasets used for analysis and mapping.
- **`treeroute/`**: Contains the interactive map files (`map.html`) for visualization.
- **`scripts/`**: Contains utility scripts for data preparation.

## Running the Project

### Windows Users:
- Double-click **`run_report.bat`** in the root folder to start the server.
- Double-click **`run_model.bat`** in the root folder to update the risk model.

### MacOS/Linux Users:
To view the **Full Project Report** (including the embedded map):
1. Open a terminal in the root directory.
2. Start a local server:
   ```bash
   python3 -m http.server 8000
   ```
3. Open your browser and go to: `http://localhost:8000/Report/index.html`

---

## Technical: Running the Model Standalone

To process new sensor data and update the risk indices:
1. Open a terminal and navigate to the `Artefact` directory:
   ```bash
   cd Artefact
   ```
2. Run the model using:
   ```bash
   python3 forest_model/model.py
   ```

## Technical: Running the Map Standalone

To view the interactive map directly:
1. Open a terminal and navigate to the `Artefact` directory:
   ```bash
   cd Artefact
   ```
2. Start a local server:
   ```bash
   python3 -m http.server 8000
   ```
3. Navigate to `http://localhost:8000/treeroute/map.html` in your browser.
