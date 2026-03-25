# Environmental Monitoring and Flood Risk Project

This project is a student-built system that combines sensor data, mapping, and a simple risk model to show possible flood risk in parts of Ireland.

In plain terms: it takes environmental data, processes it with a Python model, and presents the results in a visual report with an interactive map.

## What is in this project

- `Report/`: The final web report (`index.html`, `script.js`, `styles.css`, and assets).
- `Artefact/forest_model/`: Python model code (`model.py`) and model outputs.
- `Artefact/data/`: GeoJSON and CSV input data used by the map and model.
- `Artefact/treeroute/`: Interactive map files.
- `Artefact/scripts/`: Helper scripts for preparing or expanding data.

## How to view the report

From the repository root, run:

```bash
python3 -m http.server 8000
```

Then open:

`http://localhost:8000/Report/index.html`

## How to run the model

From the repository root, run:

```bash
cd Artefact
python3 forest_model/model.py
```

This updates the model output files in `Artefact/forest_model/`.

## Optional: open the map directly

With the local server running, open:

`http://localhost:8000/Artefact/treeroute/map.html`

## Notes

- If a map or asset does not load, make sure you started a local server and did not open the HTML file directly.
- This repository includes project work from development and reporting stages, so files are grouped by purpose rather than as a production app.
