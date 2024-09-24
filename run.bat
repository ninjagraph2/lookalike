@echo off

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
timeout /t 5 > NUL
start "" http://127.0.0.1:7860
pause