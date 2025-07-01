import unittest
from datetime import datetime, timedelta
from src.log_parser import JobEvent
from src.report_generator import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def test_generate_report(self):
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
        report_gen = ReportGenerator(timedelta(minutes=5), timedelta(minutes=10))
        report = report_gen.generate_report(jobs)
        status_map = {r['pid']: r['status'] for r in report}
        self.assertEqual(status_map['1'], 'OK')
        self.assertEqual(status_map['2'], 'WARNING')
        self.assertEqual(status_map['3'], 'ERROR')

    def test_incomplete_job(self):
        jobs = {'4': JobEvent('4', 'D')}
        now = datetime(2025, 7, 1, 12, 0, 0)
        jobs['4'].set_time('START', now)
        report_gen = ReportGenerator(timedelta(minutes=5), timedelta(minutes=10))
        report = report_gen.generate_report(jobs)
        self.assertEqual(report[0]['status'], 'INCOMPLETE')

if __name__ == '__main__':
    unittest.main()
