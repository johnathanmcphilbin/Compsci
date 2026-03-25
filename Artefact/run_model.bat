@echo off
echo Running Forest Disaster Risk Model...
cd Artefact
python forest_model/model.py
echo.
echo Processing complete. Results saved to Artefact/forest_model/results.json
echo.
pause
