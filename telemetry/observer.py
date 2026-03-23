import requests
import telemetry.notifier as n

class DashboardObserver(n.TelemetryObserver):
    def __init__(self, url):
        self.url = url

    def update(self, stats: dict):
        try:
            #print("PRINTING REQUETSS")
            requests.post(self.url, json=stats)
        except Exception:
            pass 