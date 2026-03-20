# now basically is ne karna kia
# input na data read karna ha 

# find which index (column number) corresponds to your internal names

# iske bad core ko sirf wo read karna ata ha jo config.json mai mentioned ha
# to dictionary banani of keys(wo naam jo conifg mai ha )aur values data sset ss

# ya function packet return karega jo main multiprocessing queue mai dal dega
import csv
import time

type_functions = {
    "float": float,
    "integer": int,
    "string": str
}

def read_data_file(path_of_File,data_schema,raw_data_queue,input_speed):
    #read the file
    print(path_of_File)
    print(data_schema)
    print(raw_data_queue)
    print(input_speed)
    with open(path_of_File,mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        index_mapping = {}
   #now creating an index of form
        # index_mapping{
        #     "enitity_name" : {
        #         "index" : 0
        #         "type": string
        #     }
        # }

        for idx,h in enumerate(headers):
            for c in data_schema["columns"]:
                # print(c)
                if c["source_name"].strip().lower() == h.strip().lower():
                    #match mil gaya
                    index_mapping[c["internal_mapping"]]={
                        "index" : idx,
                        "type" : c["data_type"]
                    }
                    break
            print(index_mapping)
      
     
        idx = 0
        # print("INDEX")
        # print(index_mapping)
        for row in reader:
            packet = {}
            for i in index_mapping:
                temp = index_mapping[i]
                cast_func = type_functions.get(temp["type"], str) 
                packet[i] = cast_func(row[temp["index"]])
                packet["id"] = idx
                # print("in loop", packet)
            idx += 1
            # print("outerLoop",packet)
            raw_data_queue.put(packet)
            current_size = raw_data_queue.qsize()
            # print(f"Items waiting in Raw Stream: {current_size}")
            # time.sleep(input_speed)
            time.sleep(input_speed)

    #map the raw column names as mentioned in config
#       "schema_mapping": {
#     "columns": [
#       {
#         "source_name": "Sensor_ID",
#         "internal_mapping": "entity_name",
#         "data_type": "string"
#       },
#       {
#         "source_name": "Timestamp",
#         "internal_mapping": "time_period",
#         "data_type": "integer"
#       },
#       {
#         "source_name": "Raw_Value",
#         "internal_mapping": "metric_value",
#         "data_type": "float"
#       },
#       {
#         "source_name": "Auth_Signature",
#         "internal_mapping": "security_hash",
#         "data_type": "string"
#       }
#     ]
#   },

    return 0