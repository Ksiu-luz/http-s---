import unittest
import client
import os


class Test(unittest.TestCase):
    os.chdir("tests")

    def test_get(self):
        self.assertEqual(
            client.start(
                "https://jsonplaceholder.typicode.com/posts/1",
                "GET",
                "Accept:text/html",
                300,
                None,
                None,
            ).status_code,
            200,
        )

    def test_get2(self):
        self.assertEqual(
            client.start(
                "https://jsonplaceholder.typicode.com/posts/2",
                "GET",
                None,
                300,
                None,
                None,
            ).status_code,
            200,
        )

    def test_post(self):
        self.assertEqual(
            client.start(
                "https://jsonplaceholder.typicode.com/posts/1",
                "POST",
                None,
                300,
                None,
                "hello",
            ).status_code,
            404,
        )
    
    
    def test_cookies(self):
        self.assertEqual(
            client.start(
                "https://jsonplaceholder.typicode.com/posts/3",
                "GET",
                None,
                300,
                None,
                None,
            ).cookies,
            None,
        )

    def test_fall_url(self):
        self.assertEqual(
            client.start("https://dkgmdkfv/", "GET", None, 300, None, None).status_code,
            None,
        )

    def test_fall_time(self):
        self.assertEqual(
            client.start(
                "https://jsonplaceholder.typicode.com/posts/5",
                "GET",
                None,
                0,
                None,
                None,
            ).status_code,
            None,
        )

    def test_save_in_file(self):
        os.chdir("..")
        self.assertEqual(
            client.start(
                "https://jsonplaceholder.typicode.com/posts/1",
                "GET",
                "Accept:text/html",
                300,
                "file_save",
                None,
            ).status_code,
            200,
        )
        os.chdir("tests")


if __name__ == "__main__":
    unittest.main()
