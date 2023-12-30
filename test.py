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
                5,
                None,
                None,
            )[0].status_code[0],
            200,
        )

    def test_get2(self):
        self.assertEqual(
            client.start(
                "https://jsonplaceholder.typicode.com/posts/4",
                "GET"
            )[0].status_code[0],
            200,
        )
    
    def test_options(self):
        self.assertEqual(
            client.start(
                "https://jsonplaceholder.typicode.com/posts/2",
                "OPTIONS"
            )[0].status_code[0],
            204,
        )
    
    def test_post(self):
        self.assertEqual(
            client.start(
                "https://jsonplaceholder.typicode.com/posts",
                "POST",\
                data="Data:bobobo"
            )[0].status_code[0],
            201,
        )
    
    def test_head(self):
        self.assertEqual(
            client.start(
                "https://jsonplaceholder.typicode.com/posts/3",
                "HEAD"
            )[0].status_code[0],
            200,
        )
    
    def test_cookies(self):
        self.assertEqual(
            client.start(
                "https://jsonplaceholder.typicode.com/posts/3",
                "GET"
            )[1],
            None,
        )

    def test_small_time(self):
        self.assertEqual(
            client.start(
                "https://jsonplaceholder.typicode.com/posts/5",
                "GET",
                timeout=1
            )[0].status_code[0],
            200,
        )

    def test_save_in_file(self):
        os.chdir("..")
        self.assertEqual(
            client.start(
                "https://jsonplaceholder.typicode.com/posts/1",
                "GET"
            )[0].status_code[0],
            200,
        )
        os.chdir("tests")


if __name__ == "__main__":
    unittest.main()
