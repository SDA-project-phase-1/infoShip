@echo off
pip install -r requirements.txt
cd dashboard
call npm install
cd ..
echo Setup Complete. Run the project with: python main.py
pause