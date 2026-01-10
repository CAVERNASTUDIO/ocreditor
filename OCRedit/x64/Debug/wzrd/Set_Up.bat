@echo off
REM ============================================================
REM Script para instalar librerías necesarias del proyecto OCR 
REM Autor: Ing. Erik Alejandro García Aparicio
REM Fecha: 2025
REM copyright (c) - 2025 Erik Alejandro García Aparicio 
REM ============================================================

echo Instalando dependencias de Python para el software...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Python no está instalado o no está en el PATH.
    echo Descarga e instala Python desde https://www.python.org/downloads/
    exit /b 1
)

REM Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip

pause
REM Bibliotecas de eficiencia
pip install numpy
pip install pandas
pip install scipy
pip install cython
pip install joblib
pip install psutil
pip install memory-profiler

REM Bibliotecas de seguridad
pip install pycryptodome
pip install cerberus
pip install bandit

REM Instalar librerías necesarias
echo Instalando librerías: pypdf y Pillow...
python -m pip install pypdf pillow
pip install PyPDF2
pip install pikepdf
pip install pdfplumber
pip install reportlab
pip install opencv-python
pip install imageio
pip install pydub
pip install soundfile
pip install librosa
pip install python-docx
pip install python-pptx
pip install openpyxl
pip install xlrd

echo.
echo Instalando paquetes: psutil pyusb pybluez
%PIP_CMD% install psutil pyusb pybluez
if %ERRORLEVEL% equ 0 (
    echo.
    echo Instalacion completada correctamente.
) else (
    echo.
    echo Hubo errores durante la instalacion. Revisa la salida anterior para detalles.
    echo Nota: pybluez puede requerir dependencias de compilacion (Build Tools) en Windows.
)

echo Instalando paquetes base: numpy matplotlib...
pip install --upgrade numpy matplotlib
if %errorlevel% neq 0 (
    echo ERROR: Fallo instalando numpy/matplotlib.
    exit /b 1
)

REM --- Instalar Qt para Python segun configuracion ---
if "%USE_PYSIDE6%"=="1" (
    echo Instalando PySide6 (Qt for Python)...
    pip install --upgrade PySide6
    if %errorlevel% neq 0 (
        echo ERROR: Fallo instalando PySide6.
        exit /b 1
    )
) else (
    echo Instalando PyQt5...
    pip install --upgrade PyQt5
    if %errorlevel% neq 0 (
        echo ERROR: Fallo instalando PyQt5.
        exit /b 1
    )
)

:: Instalar tkinterdnd2
echo Instalando tkinterdnd2...
python -m pip install tkinterdnd2

:: Verificar instalación
echo Verificando instalación...
python -c "import tkinterdnd2; print('tkinterdnd2 instalado correctamente')"



echo.
echo [OK] Instalación completada.
echo Ahora puedes ejecutar tu script principal con:
echo python tu_script.py
echo.

pause

