import sys
import unittest
from unittest.mock import patch

from app import main

class TestMain(unittest.TestCase):
    @patch('app.web.run_app')
    @patch('app.init_app')
    @patch('app.logging')
    def test_main_with_measurement_types(self, mock_logging, mock_init_app, mock_run_app):
        sys.argv = ['app.py', 'temperature', 'humidity']
        main()
        mock_init_app.assert_called_once_with(['temperature', 'humidity'])
        mock_run_app.assert_called_once()
        mock_logging.info.called_once_with("Starting service with measurement types: ['temperature', 'humidity']")
        mock_logging.info.called_once()

    @patch('app.logging')
    def test_main_without_measurement_types(self, mock_logging):
        sys.argv = ['app.py']
        with self.assertRaises(SystemExit):
            main()
        mock_logging.error.called_once_with("No measurement types provided. Exiting.")
        mock_logging.error.called_once()

if __name__ == '__main__':
    unittest.main()
