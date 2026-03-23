# Receive: The Imperative Shell pulls Packet #11 from the verified queue.
# Update: It adds the new value to its "Sliding Window" (the last 10 values).
# Calculate: The Functional Core calculates the mean of those 10 values.
# Merge: The Shell adds a new key, computed_metric, to the original packet.
# Emit: It sends that single, "fat" packet to processed queue.
import heapq
import time
def cal_avg(window):
    if not window:
        return 0.0
    return sum(window) / len(window)

def aggregating_from_intermediate_stream(intermediate_stream,processed_data_Stream,window_size):
    window = []
    pq = []

    expected_packet_value = 0
    while True:
        time.sleep(0.5)
        packet = intermediate_stream.get()
        if packet is None:
            break
        heapq.heappush(pq, (packet["id"], packet))

        while pq and pq[0][0] == expected_packet_value:
            heapq.heappop(pq)
            if packet["invalid_flag"] == False:
                avg = cal_avg(window)
                window.append(packet["metric_value"])

                if len(window) >= window_size:
                    window.pop(0)

                packet["computed_metric"] = cal_avg(window)

                # print("In the aggregate function")
                # print(packet)
                processed_data_Stream.put(packet)
                # time.sleep(1)
            expected_packet_value += 1

