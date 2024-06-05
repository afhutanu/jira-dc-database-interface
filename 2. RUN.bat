@echo off
echo Starting Docker container...
start /b docker run -p 5000:5000 flask-app
echo Waiting for the server to start...
timeout /t 5
echo Opening browser...
start http://localhost:5000
echo Container started and browser opened.
pause