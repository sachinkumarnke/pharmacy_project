@echo off
echo Building Docker image...
docker build -t pharmacy-app .
echo Docker image built successfully!
pause