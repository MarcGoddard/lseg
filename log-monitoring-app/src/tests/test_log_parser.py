import unittest
from datetime import datetime
from src.log_parser import LogParser, JobEvent
import os

class TestLogParser(unittest.TestCase):
    def setUp(self):
        self.test_log = 'test_logs.log'
        with open(self.test_log, 'w', encoding='utf-8') as f:
            f.write('2025-07-01 12:00:00,Job A,START,1001\n')
            f.write('2025-07-01 12:06:00,Job A,END,1001\n')
            f.write('2025-07-01 12:10:00,Job B,START,1002\n')
            f.write('2025-07-01 12:21:00,Job B,END,1002\n')
            f.write('malformed,row,should,skip\n')
            f.write('notadate,Job D,START,1004\n')

    def tearDown(self):
        os.remove(self.test_log)

    def test_parse_log_file(self):
        jobs = LogParser.parse_log_file(self.test_log)
        self.assertIn('1001', jobs)
        self.assertIn('1002', jobs)
        self.assertEqual(jobs['1001'].duration(), 360.0)
        self.assertEqual(jobs['1002'].duration(), 660.0)
        self.assertNotIn('1004', jobs)

    def test_parse_datetime(self):
        self.assertIsNotNone(LogParser.parse_datetime('2025-07-01 12:00:00'))
        self.assertIsNone(LogParser.parse_datetime('notadate'))

if __name__ == '__main__':
    unittest.main()
