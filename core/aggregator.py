# Receive: The Imperative Shell pulls Packet #11 from the verified queue.
# Update: It adds the new value to its "Sliding Window" (the last 10 values).
# Calculate: The Functional Core calculates the mean of those 10 values.
# Merge: The Shell adds a new key, computed_metric, to the original packet.
# Emit: It sends that single, "fat" packet to processed queue.