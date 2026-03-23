import core.verification as ver
import time

def core_main_work(raw_data_stream,intermediate_avg_data,input_delay,core_config):
    while True:
        packet = raw_data_stream.get()
        if packet is None:
            raw_data_stream.put(None)
            break
        packet["invalid_flag"] = False
        print(f"Core received: {packet["id"]}",end="")
        print(f" Raw Stream: {raw_data_stream.qsize()}",end="")
        print(f" intermediate Stream: {intermediate_avg_data.qsize()}",end="")
        # print(f" processed Stream: {intermediate_avg_data.qsize()}",end="")
        if ver.verify_the_signature(packet["security_hash"],core_config["stateless_tasks"]["secret_key"],core_config["stateless_tasks"]["iterations"],str(packet["metric_value"])) == True:
            intermediate_avg_data.put(packet)
            print(" ✅VALID DATA")
        else:
            packet["metric_value"] = 0
            packet["security_hash"] =  ""
            packet["time_period"] =  0
            packet["entity_name"] =  ""
            packet["invalid_flag"] = True
            intermediate_avg_data.put(packet)
            print(" ❌ INVALID PACKET HAA")
        # time.sleep(input_delay)




    
