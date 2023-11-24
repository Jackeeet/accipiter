import json
import sys


class LogManager:

    def __init__(self):
        config_path = sys.path[0] + "/config.json"
        with open(config_path, 'r') as file:
            self._cfg = json.load(file)["logs"]
        self.active = self._cfg["log_alerts"]
        self.error_log = self._cfg["error_log_path"]
        self.alert_log = self._cfg["alert_log_path"]
        self.event_log = self._cfg["event_log_path"]

    def log_error(self, error: str):
        if self.active:
            with open(sys.path[0] + self.error_log, 'w+') as err_log:
                err_log.write(error)
                err_log.write('\n')

    def log_event(self, event: str):
        if self.active:
            with open(sys.path[0] + self.event_log, 'w+') as evt_log:
                evt_log.write(event)
                evt_log.write('\n')

    def log_alert(self, alert: str):
        if self.active:
            with open(sys.path[0] + self.alert_log, 'w+') as alt_log:
                alt_log.write(alert)
                alt_log.write('\n')
