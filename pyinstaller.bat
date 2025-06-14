@echo off
pyinstaller TorchManager.spec
cd /d "%~dp0dist"
TorchManager.exe
PAUSE