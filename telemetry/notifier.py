from abc import ABC, abstractmethod
import threading
import time
import multiprocessing
class TelemetryObserver(ABC):
    @abstractmethod
    def update(self, stats: dict):
        pass


class PipelineTelemetry:
    def __init__(self,queues : dict,poll_interval=0.5):
        self.queues = queues
        self.poll_interval = poll_interval
        self.observers = [] # List of subscribers
        self._running = True

    def subscribe(self,observer :TelemetryObserver ):
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(self,observer :TelemetryObserver ):
        if observer  in self.observers:
            self.observers.remove(observer)

    def notify(self,stats):
        for o in self.observers:
            o.update(stats)

    def start_monitoring(self):
        proc = multiprocessing.Process(target=self.monitor_Wali_loop)
        proc.daemon = True
        proc.start()
        return proc


    def monitor_Wali_loop(self):
        print(" Telemetry Process Started...")
        try:
            while self._running:
                print(" Telemetry Process Started...")
                stats = {}
                # FIX: Added () to .items()
                for name, q in self.queues.items():
                    stats[name] = q.qsize()
                
                # FIX: Used self._observers inside notify()
                self.notify(stats)
                time.sleep(self.poll_interval)
        except Exception as e:
            print(f"Telemetry Loop Crashed: {e}")




    