import csv
import logging
from datetime import datetime
from typing import Dict, Optional

class JobEvent:
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

    def duration(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

class LogParser:
    DATE_FORMATS = [
        '%Y-%m-%d %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
        '%H:%M:%S'
    ]

    @staticmethod
    def parse_datetime(dt_str: str, fallback_date: Optional[datetime]=None) -> Optional[datetime]:
        dt_str = dt_str.strip()
        for fmt in LogParser.DATE_FORMATS:
            try:
                dt = datetime.strptime(dt_str, fmt)
                if fmt == '%H:%M:%S' and fallback_date:
                    return fallback_date.replace(hour=dt.hour, minute=dt.minute, second=dt.second)
                return dt
            except ValueError:
                continue
        logging.warning(f"Unrecognized datetime format: {dt_str}")
        return None

    @staticmethod
    def parse_log_file(filepath: str) -> Dict[str, JobEvent]:
        jobs: Dict[str, JobEvent] = {}
        fallback_date = None
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) != 4:
                        logging.warning(f"Skipping malformed row: {row}")
                        continue
                    timestamp_str, description, event_type, pid = row
                    timestamp = LogParser.parse_datetime(timestamp_str, fallback_date)
                    if not timestamp:
                        continue
                    if not fallback_date:
                        fallback_date = timestamp
                    pid = pid.strip()
                    description = description.strip()
                    event_type = event_type.strip().upper()
                    if pid not in jobs:
                        jobs[pid] = JobEvent(pid, description)
                    jobs[pid].set_time(event_type, timestamp)
        except FileNotFoundError:
            logging.error(f"Log file '{filepath}' does not exist.")
        except Exception as e:
            logging.error(f"Error reading log file: {e}")
        return jobs
