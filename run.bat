@echo off

REM Проверяем наличие пакетов из requirements.txt
python -c "import sys, pkg_resources; sys.exit(len([r for r in pkg_resources.parse_requirements(open('requirements.txt')) if not pkg_resources.working_set.find(r)]));" 2>NUL
if %errorlevel% equ 0 (
    echo requirements already installed.
) else (
    echo Requirements not found, creating venv...
    
    py -m venv lookalike_venv
    echo Venv created!
    call lookalike_venv\Scripts\activate
	echo Venv activated!
    
    echo Requirements installing...
    pip install --upgrade pip
    pip install --no-cache-dir -r requirements.txt
)

REM Запускаем приложение
echo.
echo      @@@@@@@@@@@           
echo   @@@@@@   @@@@@@@         
echo  @@@@           @@@@       
echo @@@         @@@@@@@@@@     
echo @@@      @@@@@@@@@@@@@@@   
echo @@@     @@@@@     @@@@@@@@ 
echo @@@    @@@        @@@  @@@@
echo @@@@  @@@        @@     @@@
echo  @@@@@@@@      @ @@     @@@
echo    @@@@@@  @@ @@@       @@@
echo       @@@@@@@          @@@@
echo        @@@@           @@@@ 
echo         @@@@@@@    @@@@@@  
echo            @@@@@@@@@@@@    
gradio app.py
pause