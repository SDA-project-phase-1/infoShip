=========================================================
infoShip - Real-Time Data Pipeline & Dashboard
=========================================================

1. SETUP (Choose one):
----------------------
A. Automatic: 
   Double-click 'setup.bat' in the root folder.

B. Manual:
   pip install -r requirements.txt
   cd dashboard
   npm install
   cd ..

2. RUN:
-------
   python main.py

3. DIRECTORY LOCATIONS:
-----------------------
- Main File: /main.py (Run this)
- Data:      /data/ (Place CSV here)
- Config:    /config.json
- Dashboard: /dashboard/

4. OUTPUT:
----------
The dashboard will open automatically at http://localhost:3000
using a Node.js server with Express and Socket.io.
=========================================================