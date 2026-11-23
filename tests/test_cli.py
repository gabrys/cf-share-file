import subprocess
import sys
import unittest


class CommandTests(unittest.TestCase):
    def test_help_without_cloudflared(self):
        result = subprocess.run(
            [sys.executable, "-m", "cf_share_file", "--help"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("--auth", result.stdout)
        self.assertNotIn("--port", result.stdout)

    def test_port_option_is_rejected(self):
        result = subprocess.run(
            [sys.executable, "-m", "cf_share_file", "example.txt", "--port", "8080"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments: --port", result.stderr)

    def test_missing_file_is_rejected(self):
        result = subprocess.run(
            [sys.executable, "-m", "cf_share_file", "nonexistent-file-for-test"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("not a file", result.stderr)
