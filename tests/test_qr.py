import contextlib
import io
import subprocess
import sys
import unittest
from unittest.mock import patch

import cf_share_file


URL = "https://example.trycloudflare.com/report%20file.pdf"


class QRTests(unittest.TestCase):
    def test_url_without_site_packages(self):
        result = subprocess.run(
            [sys.executable, "-S", "-c",
             f"from cf_share_file import print_public_url; print_public_url({URL!r})"],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(result.stdout, URL + "\n")
        self.assertEqual(result.stderr, "")

    def test_qr_goes_to_stderr_and_contains_full_url(self):
        try:
            import qrcode
        except ImportError:
            self.skipTest("qrcode is not installed")
        stdout, stderr = io.StringIO(), io.StringIO()
        original_add_data = qrcode.QRCode.add_data
        added = []

        def capture_data(qr, data, *args, **kwargs):
            added.append(data)
            return original_add_data(qr, data, *args, **kwargs)

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            with patch.object(qrcode.QRCode, "add_data", capture_data):
                cf_share_file.print_public_url(URL)
        self.assertEqual(stdout.getvalue(), URL + "\n")
        self.assertEqual(added, [URL])
        self.assertTrue(stderr.getvalue().strip())

    def test_oversized_url_still_prints_url(self):
        try:
            import qrcode
        except ImportError:
            self.skipTest("qrcode is not installed")
        url = URL + "x" * 10000
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            cf_share_file.print_public_url(url)
        self.assertEqual(stdout.getvalue(), url + "\n")
        self.assertIn("QR code unavailable", stderr.getvalue())
