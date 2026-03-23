# infoShip
========================================================================
PROJECT: infoShip - Concurrent Real-Time Data Pipeline & Dashboard
========================================================================

1. OVERVIEW
This project is a high-performance data processing pipeline utilizing:
- Python Multiprocessing (Scatter-Gather Pattern)
- Observer Design Pattern for Pipeline Telemetry
- Node.js, Express, and Socket.io for Real-Time Data Visualization
- Dependency Inversion via Functional Core / Imperative Shell architecture

2. DIRECTORY STRUCTURE & FILE LOCATIONS
The project is organized as follows:

- MAIN ENTRY POINT: /main.py (Root directory)
- DATA FILES:      /data/ 
  (Place your unseen sensor_data.csv here)
- CONFIG FILES:    /config.json (Root directory)
  (Place your modified JSON configuration here)
- TELEMETRY LOGIC: /telemetry/ (Contains Notifier and Observer logic)
- PROCESSING CORE: /core/ (Contains mainClass and Aggregator logic)
- DASHBOARD:       /dashboard/ (Contains server.js and UI components)

3. PREREQUISITES
Ensure you have the following installed:
- Python 3.8+
- Node.js & npm

4. INSTALLATION & SETUP
To install all necessary Python dependencies, open your terminal in the 
project root and run:

    pip install -r requirements.txt

For the Node.js server, navigate to the dashboard folder:

    cd dashboard
    npm install

5. HOW TO RUN
You only need to run the main Python file. It is designed as an 
"Imperative Shell" that will automatically:
- Launch the Node.js Express server as a subprocess.
- Open your default Web Browser to http://localhost:3000.
- Initialize the multiprocessing streams and telemetry.

To start the system, run from the root directory:

    python main.py

6. TELEMETRY & OUTPUT
The output is displayed via a web-based dashboard using Web Browser JS 
and Sockets. 

In accordance with the Observer Pattern requirements:
- The PipelineTelemetry (Subject) polls queue sizes independently.
- The Dashboard (Observer) reflects these via real-time color codes:
  * GREEN: Flowing smoothly (Queue < 30%)
  * YELLOW: Filling up (Queue > 30%)
  * RED: Heavy Backpressure (Queue > 70%)

========================================================================