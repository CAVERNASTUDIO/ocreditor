@echo off
cd /d "%~dp0"
title OCREDIT
color 0A
:menu
echo ===============================
echo             OCREDITOR 
echo===============================
echo Menu de herramientas
echo ==============================
echo 1. OCR IMG PDF
echo 2. OCR Bloqueo de Documentos 
echo                             "e" to exit
echo ==============================
echo Copyright (c) - 2025 Erik Alejandro García Aparicio. all rigths reserved.
set /p opcion=Ingrese el número de opción (1-2): 

if "%opcion%"=="1" goto opcion1
if "%opcion%"=="2" goto opcion2
if "%opcion%"=="e" goto opcione

echo Opción inválida. Intente de nuevo.
pause
cls
goto menu

:opcion1
python IMPDF.py
pause
cls
goto menu

:opcion2
python BloqueoDocumentos.py
pause
cls
goto menu

:opcione 
exit /b 0

pause


