import time

class LogCollector:
    def __init__(self, log_file="/var/log/syslog"):
        self.log_file = log_file
        
    def tail(self):
        """Generator to yield new lines from the log file in real-time."""
        with open(self.log_file, 'r') as f:
            f.seek(0, 2)
            while True:
                try:
                    line = f.readline()
                    if not line:
                        time.sleep(0.01)
                        continue
                    yield line.strip()
                  
                except KeyboardInterrupt:
                    print("Log collection interrupted.")
                    break
                
    def collect_logs(self):
        """Collect logs in real-time and return them."""
        return self.tail()