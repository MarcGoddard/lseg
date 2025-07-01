# Log Monitoring Application

This application monitors job durations from a CSV log file and reports warnings or errors if jobs exceed specified time thresholds. It now supports logs spanning multiple days, CLI arguments, export to CSV/JSON, and improved error handling.

## Features
- Parses a CSV log file (`logs.log`).
- Supports logs spanning multiple days (date + time in log entries).
- Tracks job start and end times using PID.
- Calculates job durations.
- Logs a warning if a job exceeds a configurable threshold (default: 5 minutes).
- Logs an error if a job exceeds a configurable threshold (default: 10 minutes).
- CLI arguments for log file path and thresholds.
- Export report to CSV or JSON.
- More robust error handling and logging.
- Improved code structure (functions, main, etc).
- Clean, secure, and well-documented code.
- Includes automated tests.

## Usage
1. Place your `logs.log` file in the project directory (or specify another file with `--logfile`).
2. Run the application:
   ```sh
   python log_monitor.py --logfile logs.log --warning 5 --error 10 --export report.csv --format csv
   ```
   - `--logfile`: Path to the log file (default: logs.log)
   - `--warning`: Warning threshold in minutes (default: 5)
   - `--error`: Error threshold in minutes (default: 10)
   - `--export`: Export the report to a file (CSV or JSON)
   - `--format`: Export format: csv or json (default: csv)
3. View the output report in the console and/or in the exported file.

## Code Quality & Security Practices
- Input validation and robust error handling are implemented.
- Follows PEP8 (Python style guide) and OWASP secure coding practices.
- Comments explain complex logic.
- Automated tests included using `unittest`.

## References
- [PEP8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [argparse — Parser for command-line options](https://docs.python.org/3/library/argparse.html)
- [Python logging best practices](https://docs.python.org/3/howto/logging.html)

## License
See LICENSE file.
