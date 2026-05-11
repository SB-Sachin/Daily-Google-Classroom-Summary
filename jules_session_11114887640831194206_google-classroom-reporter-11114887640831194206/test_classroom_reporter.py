import unittest
from unittest.mock import MagicMock, patch
import datetime
import classroom_reporter

class TestClassroomReporter(unittest.TestCase):

    @patch('classroom_reporter.build')
    @patch('classroom_reporter.get_credentials')
    def test_get_report_no_courses(self, mock_get_creds, mock_build):
        mock_get_creds.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        mock_service.courses().list().execute.return_value = {"courses": []}
        
        report = classroom_reporter.get_report()
        self.assertEqual(report, "No active courses found.")

    @patch('classroom_reporter.build')
    @patch('classroom_reporter.get_credentials')
    def test_get_report_with_data(self, mock_get_creds, mock_build):
        mock_get_creds.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        today = datetime.datetime.now(datetime.timezone.utc)
        today_str = today.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        mock_service.courses().list().execute.return_value = {
            "courses": [{"id": "123", "name": "Math"}]
        }
        
        mock_service.courses().announcements().list().execute.return_value = {
            "announcements": [{"creationTime": today_str, "text": "Learned Algebra today"}]
        }
        
        mock_service.courses().courseWork().list().execute.return_value = {
            "courseWork": [
                {
                    "title": "Homework 1",
                    "creationTime": today_str,
                    "dueDate": {"year": today.year, "month": today.month, "day": today.day}
                }
            ]
        }
        
        report = classroom_reporter.get_report()
        self.assertIn("Course: Math", report)
        self.assertIn("Learned Algebra today", report)
        self.assertIn("Homework 1", report)

if __name__ == '__main__':
    unittest.main()
