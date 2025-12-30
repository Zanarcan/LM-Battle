@echo off
echo.
echo ========================================
echo   ART PROJECT - DASHBOARD LAUNCHER
echo ========================================
echo.
echo Iniciando Streamlit Dashboard...
echo.
echo El navegador se abrira automaticamente en:
echo http://localhost:8501
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

cd /d "%~dp0"
start http://localhost:8501
streamlit run streamlit_app.py

pause
