@echo off
cd /d "%~dp0"
title OCREDIT
color 0A
:menu
echo ===============================
echo             OCREDITOR 
echo===============================
echo Tools
echo ==============================
echo 1. OCR Proyects
echo 2. OCR Lock 
echo 3. OCR Integrates Formats
echo 4. OCR Tool
echo 5. OCR Translator
echo                             "e" to exit
echo ==============================
echo Copyright (c) - 2025, 2026 Erik Alejandro García Aparicio. all rigths reserved.
set /p opcion=Selection (1-5): 

if "%opcion%"=="1" goto opcion1
if "%opcion%"=="2" goto opcion2
if "%opcion%"=="3" goto opcion3
if "%opcion%"=="4" goto opcion4
if "%opcion%"=="5" goto opcion5
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

:opcion3
python integra_formatos.py
pause
cls
goto menu

:opcion4
python Pil.py
pause
cls
goto menu

:opcion5
python Traslate.py
pause
cls
goto menu

:opcione 
exit /b 0

pause




