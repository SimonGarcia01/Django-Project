import time
from django.test import TestCase
from unittest.mock import patch, MagicMock
from psycopg2 import OperationalError

from wait_for_db import wait_for_postgres


class WaitForDBTests(TestCase):

    @patch("wait_for_db.psycopg2.connect")
    @patch("wait_for_db.time.sleep")
    def test_waits_until_db_available(self, mock_sleep, mock_connect):
        """
        Simulate Postgres failing at first, then becoming available.
        """
        # First call raises OperationalError, second call returns success
        mock_connect.side_effect = [OperationalError(), MagicMock()]

        wait_for_postgres()

        # connect() should be called twice
        self.assertEqual(mock_connect.call_count, 2)

        # sleep() should be called once
        mock_sleep.assert_called_once_with(1)

    @patch("wait_for_db.psycopg2.connect")
    def test_immediate_success(self, mock_connect):
        """
        If Postgres is available immediately, no retries occur.
        """
        mock_connect.return_value = MagicMock()

        wait_for_postgres()

        # Should only connect once
        self.assertEqual(mock_connect.call_count, 1)
