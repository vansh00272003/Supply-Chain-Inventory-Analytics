@echo off
TITLE Walmart-Style Supply Chain Analytics - Offline Power BI Dashboard Launcher
CLS

echo ===============================================================================
echo        WALMART-STYLE SUPPLY CHAIN & INVENTORY ANALYTICS DASHBOARD
echo                       OFFLINE POWER BI DESKTOP LAUNCHER
echo ===============================================================================
echo.

SET "PBIX_PATH=%~dp0walmart_style_supply_chain_dashboard.pbix"
SET "EXCEL_PATH=%~dp0..\data\walmart_style_supermarket_supply_chain_dataset.xlsx"

echo [1/2] Verifying local dataset availability...
IF EXIST "%EXCEL_PATH%" (
    echo     SUCCESS: Found dataset at %EXCEL_PATH%
) ELSE (
    echo     WARNING: Dataset not found at %EXCEL_PATH%!
)
echo.

echo [2/2] Opening native Power BI Report file (.pbix)...
IF EXIST "%PBIX_PATH%" (
    echo     SUCCESS: Found Power BI Report at %PBIX_PATH%
    START "" "%PBIX_PATH%"
) ELSE (
    echo     Opening excel loaded.pbix...
    START "" "%~dp0excel loaded.pbix"
)

echo.
echo ===============================================================================
echo Dashboard launched! Power BI Desktop will open your native multi-page report.
echo ===============================================================================
echo.
TIMEOUT /T 5
