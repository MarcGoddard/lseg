
import csv
import logging
import argparse
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import os
import sys

# Configure logging for warnings and errors
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

DATE_FORMATS = [
    '%Y-%m-%d %H:%M:%S',  # preferred: 2025-07-01 12:00:00
    '%d/%m/%Y %H:%M:%S',  # alt: 01/07/2025 12:00:00
    '%m/%d/%Y %H:%M:%S',  # alt: 07/01/2025 12:00:00
    '%H:%M:%S'            # fallback: time only (assume same day)
]

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

def parse_datetime(dt_str: str, fallback_date: Optional[datetime]=None) -> Optional[datetime]:
    dt_str = dt_str.strip()
    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(dt_str, fmt)
            if fmt == '%H:%M:%S' and fallback_date:
                # If only time is provided, use fallback date
                return fallback_date.replace(hour=dt.hour, minute=dt.minute, second=dt.second)
            return dt
        except ValueError:
            continue
    logging.warning(f"Unrecognized datetime format: {dt_str}")
    return None

def parse_log_file(filepath: str) -> Dict[str, JobEvent]:
    """
    Parses the log file and returns a dictionary of JobEvents keyed by PID.
    Supports logs spanning multiple days (date + time).
    """
    jobs: Dict[str, JobEvent] = {}
    fallback_date = None
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
            # Try to parse date/time
            timestamp = parse_datetime(timestamp_str, fallback_date)
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
    return jobs

def report_job_durations(jobs: Dict[str, JobEvent], warning_threshold: timedelta, error_threshold: timedelta) -> list:
    """
    Reports job durations and logs warnings/errors based on thresholds.
    Returns a list of report dicts for export.
    """
    report = []
    for pid, job in jobs.items():
        duration = job.duration()
        entry = {
            'pid': pid,
            'description': job.description,
            'start_time': job.start_time.isoformat() if job.start_time else None,
            'end_time': job.end_time.isoformat() if job.end_time else None,
            'duration_seconds': duration.total_seconds() if duration else None,
            'status': 'OK',
            'message': ''
        }
        if duration is None:
            entry['status'] = 'INCOMPLETE'
            entry['message'] = f"Incomplete job for PID {pid} ({job.description})"
            logging.warning(entry['message'])
        elif duration > error_threshold:
            entry['status'] = 'ERROR'
            entry['message'] = f"Job PID {pid} ({job.description}) took {duration} [ERROR: >{int(error_threshold.total_seconds()//60)} minutes]"
            logging.error(entry['message'])
        elif duration > warning_threshold:
            entry['status'] = 'WARNING'
            entry['message'] = f"Job PID {pid} ({job.description}) took {duration} [WARNING: >{int(warning_threshold.total_seconds()//60)} minutes]"
            logging.warning(entry['message'])
        else:
            entry['message'] = f"Job PID {pid} ({job.description}) took {duration}"
            logging.info(entry['message'])
        report.append(entry)
    return report

def export_report(report: list, export_path: str, export_format: str):
    try:
        if export_format.lower() == 'csv':
            with open(export_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=report[0].keys())
                writer.writeheader()
                writer.writerows(report)
        elif export_format.lower() == 'json':
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
        else:
            logging.error(f"Unsupported export format: {export_format}")
    except Exception as e:
        logging.error(f"Failed to export report: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description='Log Monitoring Application')
    parser.add_argument('--logfile', type=str, default='logs.log', help='Path to log file (CSV)')
    parser.add_argument('--warning', type=int, default=5, help='Warning threshold in minutes')
    parser.add_argument('--error', type=int, default=10, help='Error threshold in minutes')
    parser.add_argument('--export', type=str, help='Export report to file (CSV or JSON)')
    parser.add_argument('--format', type=str, choices=['csv', 'json'], default='csv', help='Export format (csv or json)')
    return parser.parse_args()

def main():
    setup_logging()
    args = parse_args()
    warning_threshold = timedelta(minutes=args.warning)
    error_threshold = timedelta(minutes=args.error)
    try:
        jobs = parse_log_file(args.logfile)
        report = report_job_durations(jobs, warning_threshold, error_threshold)
        if args.export:
            export_report(report, args.export, args.format)
            logging.info(f"Report exported to {args.export} ({args.format})")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
