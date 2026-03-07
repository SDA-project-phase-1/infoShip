import input.reading_config as fr
import input.parsing_data as pd
import path as p
import multiprocessing
import os


def main():
    config_data = fr.read_config_file(p.return_config_directory())
    pipeline_settings = config_data["pipeline_dynamics"]
    data_schema = config_data["schema_mapping"]
    data_set_path = config_data["dataset_path"]
    processing_tasks = config_data["processing"]
    input_speed = pipeline_settings["input_delay_seconds"]
    num_workers = pipeline_settings["core_parallelism"]
    queue_limit = pipeline_settings["stream_queue_max_size"]
     #queues
    raw_data_stream = multiprocessing.Queue(maxsize=queue_limit) 
    processed_data_stream = multiprocessing.Queue(maxsize=queue_limit) 


    print(f"this is the path{os.path.join(p.return_base_directory(),data_set_path)}")

    input_process = multiprocessing.Process(
        target=pd.read_data_file,
        args=(os.path.join(p.return_base_directory(),data_set_path),data_schema,raw_data_stream,input_speed)
    ) #when a process is created wo file ks shru sa start karta read karna

    
    input_process.start()
    while True:
        packet = raw_data_stream.get() 
            
            # Now you can "see" the data that the Input Module sent
        print(f"Core received: {packet}")


if __name__ == "__main__": #now only one porcess will run this
    main()