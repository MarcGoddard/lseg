# Log Monitoring Application

A modular Python application for monitoring job durations from log files, reporting warnings and errors if jobs exceed specified thresholds. Now structured for maintainability and scalability.

## Project Structure

```
log-monitoring-app/
├── src/
│   ├── main.py                # Entry point of the application
│   ├── log_parser.py          # LogParser class for parsing logs
│   ├── report_generator.py    # ReportGenerator class for generating reports
│   └── tests/
│       ├── test_log_parser.py
│       └── test_report_generator.py
├── logs.log                   # Input log file
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
├── USER_GUIDE.md              # Expanded user guide
├── SECURITY_REVIEW.md         # Security/code review
└── RELEASE_NOTES.md           # Release notes
```

## Features
- Modular codebase (parser, reporting, CLI entry point)
- Parses CSV log files (supports HH:MM:SS or date+time)
- Tracks job start/end by PID, calculates durations
- Logs warnings/errors for jobs exceeding thresholds (default: 5/10 min)
- CLI arguments for log file path, thresholds, and export options
- Export report to CSV or JSON
- Robust error handling and logging
- Automated tests for each module

## Quick Start
1. Place your `logs.log` file in the project root (or specify another file with `--logfile`).
2. From the `log-monitoring-app` directory, run:
   ```sh
   python -m src.main --logfile logs.log --export output_report.csv --format csv
   ```
3. See `USER_GUIDE.md` for full usage details and examples.

## Testing
Run all tests from the project root:
```sh
python -m unittest src/tests/test_log_parser.py
python -m unittest src/tests/test_report_generator.py
```

## Documentation
- See `USER_GUIDE.md` for detailed usage and troubleshooting
- See `SECURITY_REVIEW.md` for security/code review
- See `RELEASE_NOTES.md` for version history

## License
See LICENSE file.
