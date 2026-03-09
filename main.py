import input.reading_config as fr
import input.parsing_data as pd
import path as p
import multiprocessing
import os
import subprocess
import requests
import time

url_data = "http://localhost:3000/data"
url_config = "http://localhost:3000/ui-config"
url_telemetry = "http://localhost:3000/telemetry-config"

def start_server() -> subprocess.Popen:
    path = os.path.join(p.return_base_directory(),"dashboard")
    print("Server is about to start")
    #Popen non blocking call ha , server start karke next line pa mvoe
    return subprocess.Popen(["node","server.js"],cwd = path)

def tell_server_about_config(charts_config : dict) -> None:
    #this is imp because sab config pa depend kar raha ha
    #ui kesa hona chahie ya browser ko phla batana ha
    try:
        ui_config = {}
        for idx,c in enumerate(charts_config):
            ui_config["chart_" + str(idx+ 1)] = c
        print(ui_config)
        response = requests.post(url_config,json=ui_config)
        if response.status_code == 200:
            print("Charts config sent successfully!")
    except Exception as e:
        print(f"Cannot send the config file{e}")
    

def tell_server_about_telemetry(telemetry_config: dict) -> None:
    try:
        print(f"Sending Telemetry Config: {telemetry_config}")
        
        # POST the data to the Node.js bridge
        response = requests.post(url_telemetry, json=telemetry_config)
        
        if response.status_code == 200:
            print("Telemetry config sent successfully!")
    except Exception as e:
        print(f"Failed to send telemetry: {e}")

def main() -> None:
    #starting server
    server_service = start_server()
    time.sleep(2)

    #reading config
    config_data = fr.read_config_file(p.return_config_directory())
    pipeline_settings = config_data["pipeline_dynamics"]
    data_schema = config_data["schema_mapping"]
    data_set_path = config_data["dataset_path"]
    processing_tasks = config_data["processing"]
    visualizations = config_data["visualizations"]
    telemtry_config = config_data["visualizations"]["telemetry"]
    charts_config = config_data["visualizations"]["data_charts"]
    input_speed = pipeline_settings["input_delay_seconds"]
    num_workers = pipeline_settings["core_parallelism"]
    queue_limit = pipeline_settings["stream_queue_max_size"]

    #sending config to browser
    tell_server_about_config(charts_config)
    tell_server_about_telemetry(telemtry_config)
    time.sleep(12)
    

     #queues
    raw_data_stream = multiprocessing.Queue(maxsize=queue_limit) 
    processed_data_stream = multiprocessing.Queue(maxsize=queue_limit) 
    


    print(f"this is the path{os.path.join(p.return_base_directory(),data_set_path)}")

    #Process can only do communication between python to python wale process
    #For external communciation subporcess
    input_process = multiprocessing.Process(
        target=pd.read_data_file,
        args=(os.path.join(p.return_base_directory(),data_set_path),data_schema,raw_data_stream,input_speed)
    ) #when a process is created wo file ks shru sa start karta read karna

    
    input_process.start()
    while True:
        packet = raw_data_stream.get() 
            
            # Now you can "see" the data that the Input Module sent
        print(f"Core received: {packet}")
        requests.post(url_data,json=packet)

    #end of function
    server_service.terminate()


if __name__ == "__main__": #now only one porcess will run this
    main()