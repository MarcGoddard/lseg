import logging
import csv
import json
from datetime import timedelta
from typing import Dict, List
from .log_parser import JobEvent

class ReportGenerator:
    def __init__(self, warning_threshold: timedelta, error_threshold: timedelta):
        self.warning_threshold = warning_threshold
        self.error_threshold = error_threshold

    def generate_report(self, jobs: Dict[str, JobEvent]) -> List[dict]:
        report = []
        for pid, job in jobs.items():
            duration = job.duration()
            entry = {
                'pid': pid,
                'description': job.description,
                'start_time': job.start_time.isoformat() if job.start_time else None,
                'end_time': job.end_time.isoformat() if job.end_time else None,
                'duration_seconds': duration,
                'status': 'OK',
                'message': ''
            }
            if duration is None:
                entry['status'] = 'INCOMPLETE'
                entry['message'] = f"Incomplete job for PID {pid} ({job.description})"
                logging.warning(entry['message'])
            elif duration > self.error_threshold.total_seconds():
                entry['status'] = 'ERROR'
                entry['message'] = f"Job PID {pid} ({job.description}) took {timedelta(seconds=duration)} [ERROR: >{int(self.error_threshold.total_seconds()//60)} minutes]"
                logging.error(entry['message'])
            elif duration > self.warning_threshold.total_seconds():
                entry['status'] = 'WARNING'
                entry['message'] = f"Job PID {pid} ({job.description}) took {timedelta(seconds=duration)} [WARNING: >{int(self.warning_threshold.total_seconds()//60)} minutes]"
                logging.warning(entry['message'])
            else:
                entry['message'] = f"Job PID {pid} ({job.description}) took {timedelta(seconds=duration)}"
                logging.info(entry['message'])
            report.append(entry)
        return report

    @staticmethod
    def export_report(report: List[dict], export_path: str, export_format: str):
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
