import input.reading_config as fr
import input.parsing_data as pd
import telemetry.notifier as noti
import telemetry.observer as obs
import path as p
import multiprocessing
import os
import subprocess
import requests
import time
import webbrowser
import core.mainClass as mcore
import core.aggregator as agg


url_data = "http://localhost:3000/data"
url_config = "http://localhost:3000/ui-config"
url_telemetry = "http://localhost:3000/telemetry"
url_telemetry_config = "http://localhost:3000/telemetry-config"



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
    

def tell_server_about_telemetry(telemetry_config: dict,size) -> None:
    try:
        print(f"Sending Telemetry Config: {telemetry_config}")
        telemetry_config["size"] = size
        
        # POST the data to the Node.js bridge
        response = requests.post(url_telemetry_config, json=telemetry_config)
        
        if response.status_code == 200:
            print("Telemetry config sent successfully!")
    except Exception as e:
        print(f"Failed to send telemetry: {e}")

def get_packets_from_file(raw_data_stream):
    try:
        while True:
            packet = raw_data_stream.get() 
            if packet is None:
                break
            # print(f"Core received: {packet}")
            # print(f"Stream Size (Raw): {raw_data_stream.qsize()}")
            requests.post(url_data,json=packet)
            # time.sleep(1)
    except requests.exceptions.RequestException as e:
        print(f" Network Error in Reader: {e}")
    except Exception as e:
        print(f"Unexpected Error in get_packets: {e}")

def initalizing_cores(no_of_Cores,raw_data_stream,intermediate_data_stream,processed_data_stream,processing_tasks,arr_of_process):
    try:
        for i in range(no_of_Cores):
            worker = multiprocessing.Process(
                target = mcore.core_main_work,
                args=(raw_data_stream,intermediate_data_stream,processed_data_stream,processing_tasks,)
            )
            worker.start()
            arr_of_process.append(worker)
    except Exception as e:
        print(f"Failed to initialize Cores: {e}")

def sending_response(processed_events_stream):
    try:
        while True:
            packet = processed_events_stream.get() 
            if packet is None:
                break
            # print(f"Stream Size (Processed): {processed_events_stream.qsize()}")
            response = requests.post(url_data,json=packet)
            if response.status_code == 200:
                print("✅Packet sent successfully!")
            else:
                print("❌",response.status_code)

        #print("ERRRORRRR❌❌❌❌")
    except requests.exceptions.ConnectionError:
            print("Connection Error: Is the Node.js server running?")
    except Exception as e:
        print(f"Cannot send the packet{e}")


def main() -> None:
    try:
        #?starting server
        server_service = start_server()
        # time.sleep(2)

        #?automatically opening the browser
        webbrowser.open("http://localhost:3000")
        # time.sleep(2)

        #?reading config
        config_data = fr.read_config_file(p.return_config_directory())
        pipeline_settings = config_data["pipeline_dynamics"]
        no_of_Cores = pipeline_settings["core_parallelism"]
        data_schema = config_data["schema_mapping"]
        data_set_path = config_data["dataset_path"]
        processing_tasks = config_data["processing"]
        window_size = processing_tasks["stateful_tasks"]["running_average_window_size"]
        visualizations = config_data["visualizations"]
        telemtry_config = visualizations["telemetry"]
        charts_config = visualizations["data_charts"]
        input_speed = pipeline_settings["input_delay_seconds"]
        num_workers = pipeline_settings["core_parallelism"]
        queue_limit = pipeline_settings["stream_queue_max_size"]

        #! removeeeeee
        time.sleep(3)
        #?sending config to browser
        tell_server_about_config(charts_config)
        tell_server_about_telemetry(telemtry_config,queue_limit)
      
        
        #?queues
        raw_data_stream = multiprocessing.Queue(maxsize=queue_limit) 
        intermediate_data_stream = multiprocessing.Queue(maxsize=queue_limit) 
        processed_data_stream = multiprocessing.Queue(maxsize=queue_limit) 
        
        print(f"this is the path{os.path.join(p.return_base_directory(),data_set_path)}")

        #Process can only do communication between python to python wale process
        #For external communciation subporcess

        #?All Processes
        print("Befoore  input_process")
        arr_of_process=[]
        #?First Process taking input
        input_process = multiprocessing.Process(
            target=pd.read_data_file,
            args=(os.path.join(p.return_base_directory(),data_set_path),data_schema,raw_data_stream,input_speed,)
        ) #when a process is created wo file ks shru sa start karta read karna
        # arr_of_process.append(input_process)
        print("After input_process definition")

        #?second process taking packets
        getting_packets_process = multiprocessing.Process(
            target=get_packets_from_file,
            args=(raw_data_stream,)
        )
        # arr_of_process.append(getting_packets_process)

        #?third process cores  iiniatie kar raha workers ko
        print("Before defining initializing_cores_process")
        initalizing_cores_process = multiprocessing.Process(
            target=initalizing_cores,
            args=(no_of_Cores,raw_data_stream,intermediate_data_stream,input_speed,arr_of_process,)
        )
        # arr_of_process.append(initalizing_cores_process)
        print("After defining initializing_cores_process")


        #?fourth process aggregate wala
        print("Before defining aggregating_cores_value")
        aggregating_cores_value =  multiprocessing.Process(
            target=agg.aggregating_from_intermediate_stream,
            args=(intermediate_data_stream,processed_data_stream,window_size ,)
        )
        # arr_of_process.append(aggregating_cores_value)
        print("After defining aggregating_cores_value")

        #?fifth process sending data to Node
        print("Before defining sending_response_to_server")
        sending_response_to_server = multiprocessing.Process(
            target=sending_response,
            args=(processed_data_stream,)
        )
        # arr_of_process.append(sending_response_to_server)
        print("After defining sending_response_to_server")

        queues_to_monitor = {
            "raw": raw_data_stream,
            "int": intermediate_data_stream,
            "proc": processed_data_stream
        }

        telemetry_subject = noti.PipelineTelemetry(queues_to_monitor)
        dash_observer = obs.DashboardObserver(url_telemetry)
        telemetry_subject.subscribe(dash_observer)
        telemetry_worker = telemetry_subject.start_monitoring()



        # initalizing_cores_process.start()
        initalizing_cores(no_of_Cores, raw_data_stream, intermediate_data_stream, processed_data_stream,processing_tasks,arr_of_process)
        input_process.start()
       # getting_packets_process.start()
        aggregating_cores_value.start()
        sending_response_to_server.start()
        print("After starting processes")
        
        #!creating all the process potentional masle
        # for i in arr_of_process:
        #     i.start()

        print("Before joining processes")
        # for i in arr_of_process:
        #     print(f"Waiting for {i.name} to join. Current sizes: Raw={raw_data_stream.qsize()}, Int={intermediate_data_stream.qsize()}, Proc={processed_data_stream.qsize()}")
        #     i.join()


        input_process.join() 

        for _ in range(no_of_Cores):
            raw_data_stream.put(None) 

        for worker in arr_of_process:
            worker.join()

        intermediate_data_stream.put(None)
        aggregating_cores_value.join()

        processed_data_stream.put(None)
        sending_response_to_server.join()

        telemetry_worker.terminate()
        telemetry_worker.join()

        for worker in arr_of_process:
            print(f"Waiting for Core {worker.name}...")
            worker.join()

        # initalizing_cores_process.join()
        print("After joining processes")
        
        #!joining all the process potentional masle
        # for i in arr_of_process:
        #     i.terminate()

        #?end of function
        # server_service.terminate()
    except Exception as e:
        print(f"Some Error {e}")


if __name__ == "__main__": #now only one porcess will run this
    main()