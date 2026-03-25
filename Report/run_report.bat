@echo off
echo Starting local server for Computer Science Project...
echo Once the server is running, open http://localhost:8000/Report/index.html in your browser.
echo.
echo Press Ctrl+C to stop the server.
echo.
python -m http.server 8000
pause
