import csv
import logging
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import os

# Configure logging for warnings and errors
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

LOG_FILE = 'logs.log'
TIME_FORMAT = '%H:%M:%S'
WARNING_THRESHOLD = timedelta(minutes=5)
ERROR_THRESHOLD = timedelta(minutes=10)

class JobEvent:
    """
    Represents a job event with start and end times.
    """
    def __init__(self, pid: str, description: str):
        self.pid = pid
        self.description = description
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    def set_time(self, event_type: str, timestamp: datetime):
        if event_type == 'START':
            self.start_time = timestamp
        elif event_type == 'END':
            self.end_time = timestamp

    def duration(self) -> Optional[timedelta]:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

def parse_log_file(filepath: str) -> Dict[str, JobEvent]:
    """
    Parses the log file and returns a dictionary of JobEvents keyed by PID.
    """
    jobs: Dict[str, JobEvent] = {}
    if not os.path.exists(filepath):
        logging.error(f"Log file '{filepath}' does not exist.")
        return jobs
    with open(filepath, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) != 4:
                logging.warning(f"Skipping malformed row: {row}")
                continue
            timestamp_str, description, event_type, pid = row
            try:
                timestamp = datetime.strptime(timestamp_str.strip(), TIME_FORMAT)
            except ValueError:
                logging.warning(f"Invalid timestamp format: {timestamp_str}")
                continue
            pid = pid.strip()
            description = description.strip()
            event_type = event_type.strip().upper()
            if pid not in jobs:
                jobs[pid] = JobEvent(pid, description)
            jobs[pid].set_time(event_type, timestamp)
    return jobs

def report_job_durations(jobs: Dict[str, JobEvent]):
    """
    Reports job durations and logs warnings/errors based on thresholds.
    """
    for pid, job in jobs.items():
        duration = job.duration()
        if duration is None:
            logging.warning(f"Incomplete job for PID {pid} ({job.description})")
            continue
        msg = f"Job PID {pid} ({job.description}) took {duration}"
        if duration > ERROR_THRESHOLD:
            logging.error(msg + " [ERROR: >10 minutes]")
        elif duration > WARNING_THRESHOLD:
            logging.warning(msg + " [WARNING: >5 minutes]")
        else:
            logging.info(msg)

def main():
    jobs = parse_log_file(LOG_FILE)
    report_job_durations(jobs)

if __name__ == '__main__':
    main()
