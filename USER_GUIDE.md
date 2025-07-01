# Log Monitoring Application: Expanded User Guide

This guide supplements the README and provides detailed instructions and examples for using the Log Monitoring Application.

## 1. Overview
The application analyzes job logs, calculates durations, and reports warnings or errors if jobs exceed specified thresholds. It supports logs spanning multiple days, CLI arguments, and exporting reports to CSV or JSON.

## 2. Log File Format
Each line in the log file should be a CSV entry with the following fields:

```
[timestamp],[job description],[START|END],[PID]
```
- **timestamp**: Can be `HH:MM:SS` or a full date+time (e.g., `2025-07-01 12:00:00`).
- **job description**: A description of the job or task.
- **START|END**: Indicates if the entry is the start or end of a job.
- **PID**: A unique process/job identifier.

**Example log file (`logs.log`):**
```
2025-07-01 12:00:00,Job A,START,1001
2025-07-01 12:06:00,Job A,END,1001
2025-07-01 12:10:00,Job B,START,1002
2025-07-01 12:21:00,Job B,END,1002
12:30:00,Job C,START,1003
12:45:30,Job C,END,1003
```

## 3. Running the Application

### Basic Usage
To analyze a log file and print results to the console:
```sh
python log_monitor.py --logfile logs.log
```

### Custom Thresholds
To set custom warning and error thresholds (in minutes):
```sh
python log_monitor.py --logfile logs.log --warning 3 --error 7
```

### Exporting the Report
To export the report to a CSV file:
```sh
python log_monitor.py --logfile logs.log --export report.csv --format csv
```
To export to JSON:
```sh
python log_monitor.py --logfile logs.log --export report.json --format json
```

### All CLI Options
- `--logfile`: Path to the log file (default: `logs.log`)
- `--warning`: Warning threshold in minutes (default: 5)
- `--error`: Error threshold in minutes (default: 10)
- `--export`: Export the report to a file (CSV or JSON)
- `--format`: Export format: `csv` or `json` (default: `csv`)

## 4. Output and Reporting
- **Console Output:**
  - Logs a warning if a job took longer than the warning threshold.
  - Logs an error if a job took longer than the error threshold.
  - Logs info for jobs within thresholds and incomplete jobs.
- **Exported Report:**
  - Contains job PID, description, start/end times, duration, status (OK, WARNING, ERROR, INCOMPLETE), and a message.

## 5. Example Output
**Console:**
```
WARNING: Job PID 1001 (Job A) took 0:06:00 [WARNING: >5 minutes]
ERROR: Job PID 1002 (Job B) took 0:11:00 [ERROR: >10 minutes]
ERROR: Job PID 1003 (Job C) took 0:15:30 [ERROR: >10 minutes]
```

**CSV Report:**
```
pid,description,start_time,end_time,duration_seconds,status,message
1001,Job A,2025-07-01T12:00:00,2025-07-01T12:06:00,360.0,WARNING,Job PID 1001 (Job A) took 0:06:00 [WARNING: >5 minutes]
1002,Job B,2025-07-01T12:10:00,2025-07-01T12:21:00,660.0,ERROR,Job PID 1002 (Job B) took 0:11:00 [ERROR: >10 minutes]
1003,Job C,2025-07-01T12:30:00,2025-07-01T12:45:30,930.0,ERROR,Job PID 1003 (Job C) took 0:15:30 [ERROR: >10 minutes]
```

## 6. Error Handling
- Malformed or incomplete log entries are skipped with a warning.
- Invalid date/time formats are logged as warnings.
- All file operations are safely handled with error messages for missing or inaccessible files.

## 7. Security and Best Practices
- Input validation and robust error handling are implemented.
- Follows PEP8 and OWASP secure coding standards.
- See `SECURITY_REVIEW.md` for a full security/code review.

## 8. Automated Testing
- Run all tests with:
```sh
python -m unittest test_log_monitor.py
```
- Tests cover normal, edge, and error cases.

## 9. Troubleshooting
- Ensure your log file matches the required format.
- Check console output for warnings/errors about malformed entries.
- For large files, consider exporting to CSV/JSON for easier review.

---
For further details, see the main `README.md` and `SECURITY_REVIEW.md` files.
