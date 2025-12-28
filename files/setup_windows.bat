@echo off
REM Automatic Label Printer Setup for Brother QL-700 (Windows)

echo ============================================
echo Brother QL-700 Label Printer Setup
echo ============================================
echo.

echo Step 1: Installing required Python packages...
pip install brother_ql qrcode[pil] pillow pyusb
echo.

echo Step 2: Discovering printer...
echo.
brother_ql discover
echo.

echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo To print a test label, run:
echo   python print_labels.py products.csv --test
echo.
echo To print all labels, run:
echo   python print_labels.py products.csv
echo.
pause
