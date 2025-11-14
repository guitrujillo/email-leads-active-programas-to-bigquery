@echo off
REM ========================================================================
REM Script de execucao mensal - ActiveCampaign para BigQuery
REM ========================================================================

echo ========================================================================
echo           EXTRACAO ACTIVECAMPAIGN - BIGQUERY
echo ========================================================================
echo.

REM Configura a API Key do ActiveCampaign
set ACTIVECAMPAIGN_API_KEY=ad04a29e4796290f2c213154503902af8544cbc408b13d14616c6149941db727dc258294

REM Executa o script principal
echo Iniciando extracao de dados...
echo.
python activecampaign_to_bigquery.py

echo.
echo ========================================================================
echo Deseja verificar os dados inseridos no BigQuery? (S/N)
set /p VERIFICAR=
if /i "%VERIFICAR%"=="S" (
    echo.
    python verificar_dados.py
)

echo.
echo ========================================================================
echo Processo concluido!
echo ========================================================================
pause
