@echo off
:: ============================================================
::  JALANKAN SCRAPER & EKSTRAKSI DATA
::  Klik 2x untuk mulai scraping atau ekstraksi universitas
:: ============================================================

title Scrapping Data Kasus Kekerasan Seksual
color 0A

echo.

:: Aktifkan virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo   [WARN] Virtual environment tidak ditemukan.
    echo   Jalankan SETUP_WINDOWS.bat dulu!
    pause
    exit /b 1
)

:: Cek file .env (warning saja, karena opsi 5 tidak butuh API key)
if not exist ".env" (
    echo   [WARN] File .env tidak ditemukan.
    echo   Opsi 1-4 butuh API key di .env
    echo   Opsi 5 - Ekstrak Universitas - bisa langsung jalan.
    echo.
)

python 00_jalankan_semua.py
pause
