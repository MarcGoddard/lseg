# Log Monitoring Application

This application monitors job durations from a CSV log file and reports warnings or errors if jobs exceed specified time thresholds.

## Features
- Parses a CSV log file (`logs.log`).
- Tracks job start and end times using PID.
- Calculates job durations.
- Logs a warning if a job exceeds 5 minutes.
- Logs an error if a job exceeds 10 minutes.
- Clean, secure, and well-documented code.
- Includes automated tests.

## Usage
1. Place your `logs.log` file in the project directory.
2. Run the application:
   ```sh
   python log_monitor.py
   ```
3. View the output report in the console.

## Code Quality & Security Practices
- Input validation and error handling are implemented.
- Follows PEP8 (Python style guide) and OWASP secure coding practices.
- Comments explain complex logic.
- Automated tests included using `unittest`.

## References
- [PEP8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)

## License
See LICENSE file.
