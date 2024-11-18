import psutil
import time
import logging
from datetime import datetime

logging.basicConfig(
    filename="app_monitoring.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)


def monitor_resources():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        logging.info(
            f"""
System Resources:
CPU Usage: {cpu_percent}%
Memory Usage: {memory.percent}%
Disk Usage: {disk.percent}%
        """
        )

        time.sleep(60)  # Log every minute


if __name__ == "__main__":
    monitor_resources()
