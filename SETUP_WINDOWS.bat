@echo off
:: ============================================================
::  SETUP OTOMATIS - Klik 2x file ini untuk install semua
::  yang dibutuhkan di Windows
:: ============================================================

title Social Media Scraper - Setup Windows
color 0A

echo ============================================================
echo   SETUP SOCIAL MEDIA SCRAPER - WINDOWS
echo ============================================================
echo.

:: Cek Python
echo [1/5] Mengecek Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Python belum terinstall!
    echo   Download di: https://www.python.org/downloads/
    echo   Centang "Add Python to PATH" saat install!
    pause
    exit /b 1
)
python --version
echo   [OK] Python ditemukan
echo.

:: Upgrade pip
echo [2/5] Update pip...
python -m pip install --upgrade pip --quiet
echo   [OK] pip diperbarui
echo.

:: Buat virtual environment
echo [3/5] Membuat virtual environment...
if not exist "venv" (
    python -m venv venv
    echo   [OK] Virtual environment dibuat
) else (
    echo   [SKIP] Virtual environment sudah ada
)
echo.

:: Aktifkan venv dan install package
echo [4/5] Install library Python...
call venv\Scripts\activate.bat
pip install requests pandas openpyxl python-dotenv --quiet
echo   [OK] requests, pandas, openpyxl, python-dotenv terinstall
echo.

:: Buat folder dan file .env
echo [5/5] Menyiapkan file konfigurasi...
if not exist "data" mkdir data
if not exist ".env" (
    copy .env.example .env >nul
    echo   [OK] File .env dibuat dari template
    echo   !! PENTING: Buka .env dan isi API key Anda !!
) else (
    echo   [SKIP] .env sudah ada
)
echo.

echo ============================================================
echo   SETUP SELESAI!
echo ============================================================
echo.
echo   Langkah selanjutnya:
echo   1. Buka file .env dengan Notepad
echo   2. Isi API key untuk platform yang ingin digunakan
echo   3. Klik 2x file  JALANKAN_SCRAPER.bat  untuk mulai
echo.
echo   Atau jalankan manual:
echo   ^> venv\Scripts\activate
echo   ^> python 00_jalankan_semua.py
echo.
pause
