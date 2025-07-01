import unittest
from datetime import datetime, timedelta
from log_monitor import JobEvent, parse_log_file, report_job_durations
import os

class TestJobEvent(unittest.TestCase):
    def test_duration(self):
        job = JobEvent('123', 'Test Job')
        start = datetime.strptime('12:00:00', '%H:%M:%S')
        end = datetime.strptime('12:10:00', '%H:%M:%S')
        job.set_time('START', start)
        job.set_time('END', end)
        self.assertEqual(job.duration(), timedelta(minutes=10))

    def test_incomplete_job(self):
        job = JobEvent('124', 'Incomplete Job')
        start = datetime.strptime('12:00:00', '%H:%M:%S')
        job.set_time('START', start)
        self.assertIsNone(job.duration())

class TestParseLogFile(unittest.TestCase):
    def setUp(self):
        self.test_log = 'test_logs.log'
        with open(self.test_log, 'w', encoding='utf-8') as f:
            f.write('12:00:00,Job A,START,1001\n')
            f.write('12:06:00,Job A,END,1001\n')
            f.write('12:10:00,Job B,START,1002\n')
            f.write('12:21:00,Job B,END,1002\n')
            f.write('12:30:00,Job C,START,1003\n')

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

if __name__ == '__main__':
    unittest.main()
