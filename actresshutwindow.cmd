@echo off
cd /d %~dp0
call git add .
call git commit -m "update"
call git push
call git pull
REM Check if the venv folder exists or not
if not exist venv (
    echo Creating venv folder...
    call python -m venv venv
    call venv\Scripts\activate
    REM Install the dependencies using pip
    pip install -r requirements.txt
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Run the main.py script
python main.py>outputWindow.log

call git add .
call git commit -m "update"
call git push
call git pull

REM Deactivate the virtual environment
call venv\Scripts\deactivate
