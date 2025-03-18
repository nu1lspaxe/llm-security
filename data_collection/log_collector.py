import time
from config.logging import logger

class LogCollector:
    def __init__(self, log_file="/var/log/syslog"):
        self.log_file = log_file
        logger.info(f"Initialized LogCollector with file: {self.log_file}")
        
    def tail(self):
        """Generator to yield new lines from the log file in real-time."""
        try:
            with open(self.log_file, 'r') as f:
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(0.01)
                        continue
                    yield line.strip()
        except FileNotFoundError:
            logger.error(f"Log file not found: {self.log_file}")
            raise
        except KeyboardInterrupt:
            logger.info("Log collection interrupted by user")
            raise
        except Exception as e:
            logger.error(f"Error in tailing log file: {str(e)}")
            raise
                
    def collect_logs(self):
        """Collect logs in real-time and return them."""
        return self.tail()