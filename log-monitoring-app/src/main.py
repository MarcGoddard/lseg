import argparse
import logging
from datetime import timedelta
import sys
import os
from log_parser import LogParser
from report_generator import ReportGenerator

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def parse_args():
    parser = argparse.ArgumentParser(description='Log Monitoring Application')
    parser.add_argument('--logfile', type=str, default=os.path.join(os.path.dirname(__file__), '..', '..', 'logs.log'), help='Path to log file (CSV)')
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
        jobs = LogParser.parse_log_file(args.logfile)
        report_gen = ReportGenerator(warning_threshold, error_threshold)
        report = report_gen.generate_report(jobs)
        if args.export:
            ReportGenerator.export_report(report, args.export, args.format)
            logging.info(f"Report exported to {args.export} ({args.format})")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
