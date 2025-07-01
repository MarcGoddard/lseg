import unittest
from datetime import datetime, timedelta
from log_monitor import JobEvent, parse_log_file, report_job_durations, parse_datetime
import os

class TestJobEvent(unittest.TestCase):
    def test_duration(self):
        job = JobEvent('123', 'Test Job')
        start = datetime(2025, 7, 1, 12, 0, 0)
        end = datetime(2025, 7, 1, 12, 10, 0)
        job.set_time('START', start)
        job.set_time('END', end)
        self.assertEqual(job.duration(), timedelta(minutes=10))

    def test_incomplete_job(self):
        job = JobEvent('124', 'Incomplete Job')
        start = datetime(2025, 7, 1, 12, 0, 0)
        job.set_time('START', start)
        self.assertIsNone(job.duration())

    def test_set_time_invalid_event(self):
        job = JobEvent('125', 'Invalid Event')
        now = datetime.now()
        job.set_time('INVALID', now)
        self.assertIsNone(job.start_time)
        self.assertIsNone(job.end_time)

class TestParseLogFile(unittest.TestCase):
    def setUp(self):
        self.test_log = 'test_logs.log'
        with open(self.test_log, 'w', encoding='utf-8') as f:
            f.write('2025-07-01 12:00:00,Job A,START,1001\n')
            f.write('2025-07-01 12:06:00,Job A,END,1001\n')
            f.write('2025-07-01 12:10:00,Job B,START,1002\n')
            f.write('2025-07-01 12:21:00,Job B,END,1002\n')
            f.write('2025-07-01 12:30:00,Job C,START,1003\n')
            f.write('malformed,row,should,skip\n')
            f.write('notadate,Job D,START,1004\n')

    def tearDown(self):
        os.remove(self.test_log)

    def test_parse_log_file(self):
        jobs = parse_log_file(self.test_log)
        self.assertIn('1001', jobs)
        self.assertIn('1002', jobs)
        self.assertIn('1003', jobs)
        self.assertEqual(jobs['1001'].duration(), timedelta(minutes=6))
        self.assertEqual(jobs['1002'].duration(), timedelta(minutes=11))
        self.assertIsNone(jobs['1003'].duration())
        self.assertNotIn('1004', jobs)  # Invalid date should be skipped

    def test_empty_file(self):
        empty_log = 'empty.log'
        with open(empty_log, 'w', encoding='utf-8') as f:
            pass
        jobs = parse_log_file(empty_log)
        self.assertEqual(jobs, {})
        os.remove(empty_log)

class TestParseDatetime(unittest.TestCase):
    def test_valid_formats(self):
        self.assertIsNotNone(parse_datetime('2025-07-01 12:00:00'))
        self.assertIsNotNone(parse_datetime('01/07/2025 12:00:00'))
        self.assertIsNotNone(parse_datetime('07/01/2025 12:00:00'))
        # fallback to time only
        fallback = datetime(2025, 7, 1, 0, 0, 0)
        dt = parse_datetime('12:00:00', fallback)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.year, 2025)

    def test_invalid_format(self):
        self.assertIsNone(parse_datetime('notadate'))

class TestReportJobDurations(unittest.TestCase):
    def test_report_statuses(self):
        jobs = {
            '1': JobEvent('1', 'A'),
            '2': JobEvent('2', 'B'),
            '3': JobEvent('3', 'C')
        }
        now = datetime(2025, 7, 1, 12, 0, 0)
        jobs['1'].set_time('START', now)
        jobs['1'].set_time('END', now + timedelta(minutes=4))
        jobs['2'].set_time('START', now)
        jobs['2'].set_time('END', now + timedelta(minutes=6))
        jobs['3'].set_time('START', now)
        jobs['3'].set_time('END', now + timedelta(minutes=11))
        report = report_job_durations(jobs, timedelta(minutes=5), timedelta(minutes=10))
        status_map = {r['pid']: r['status'] for r in report}
        self.assertEqual(status_map['1'], 'OK')
        self.assertEqual(status_map['2'], 'WARNING')
        self.assertEqual(status_map['3'], 'ERROR')

    def test_incomplete_job(self):
        jobs = {'4': JobEvent('4', 'D')}
        now = datetime(2025, 7, 1, 12, 0, 0)
        jobs['4'].set_time('START', now)
        report = report_job_durations(jobs, timedelta(minutes=5), timedelta(minutes=10))
        self.assertEqual(report[0]['status'], 'INCOMPLETE')

if __name__ == '__main__':
    unittest.main()
