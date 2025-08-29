@echo off
title CompactPDF - Interface Grafica
cls

echo.
echo =========================================
echo  CompactPDF - Interface Grafica
echo =========================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo.
    echo Por favor, instale o Python 3.7+ do site oficial:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python encontrado: 
python --version
echo.

REM Verificar se o arquivo GUI existe
if not exist "gui_simples.py" (
    echo ERRO: Arquivo gui_simples.py nao encontrado!
    echo.
    echo Certifique-se de executar este script no diretorio do projeto.
    echo.
    pause
    exit /b 1
)

echo Iniciando interface grafica...
echo.
echo NOTA: Esta e uma versao de demonstracao da GUI.
echo Para funcionalidade completa, configure o projeto completo.
echo.

REM Executar GUI
python gui_simples.py

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao executar a interface grafica.
    echo.
    pause
)

echo.
echo Interface grafica encerrada.
pause
