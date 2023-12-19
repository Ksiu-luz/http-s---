import unittest
import client
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import server
import threading


class Test(unittest.TestCase):

    os.chdir('tests')

    def test_get_yandex(self):
        self.assertEqual(
            client.start("https://ya.ru/", "GET", 300, "0", "").status_code, 200
        )

    def test_post_yandex(self):
        self.assertEqual(
            client.start(
                "https://ya.ru/", "POST", 300, "name_nastya_bob+age_5_99", ""
            ).status_code,
            302,
        )

    def test_post_youtube(self):
        self.assertEqual(
            client.start(
                "https://translate.yandex.ru/", "POST", 300, "name_nastya_bob+age_5_99", ""
            ).status_code,
            302,
        )

    def test_get_youtube(self):
        self.assertEqual(
            client.start("https://youtube.com/", "GET", 300, "1", "").status_code, 200
        )

    def test_cookies(self):
        self.assertGreater(
            len(client.start("https://www.youtube.com/", "GET", 300, "1", "").cookies), 0
        )

    def test_options(self):
        self.assertEqual(
            client.start("https://youtube.com/", "OPTIONS", 300, "1", "").status_code, 200
        )

    def test_head(self):
        self.assertEqual(
            client.start("https://ya.ru/", "HEAD", 300, "1", "").status_code, 302
        )

    def test_fall_url(self):
        self.assertEqual(
            client.start("https://yabbb.ru/", "GET", 300, "0", "").status_code, None
        )

    def test_fall_time(self):
        self.assertEqual(
            client.start("https://ya.ru/", "GET", 0, "0", "").status_code, None
        )


if __name__ == "__main__":
    unittest.main()
