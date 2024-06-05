@echo off
echo Building Docker image...
docker build -t flask-app .
echo Image built successfully.
pause