import unittest
import client


class Test(unittest.TestCase):
    def test_get_yandex(self):
        self.assertEqual(client.start('https://ya.ru/', 'GET', 300, '0').status_code, 200)

    def test_post_yandex(self):
        self.assertEqual(client.start('https://ya.ru/', 'POST', 300, 'name_nastya_bob+age_5_99').status_code, 302)
    
    def test_post_youtube(self):
        self.assertEqual(client.start('https://translate.yandex.ru/', 'POST', 300, 'name_nastya_bob+age_5_99').status_code, 200)
    
    def test_get_youtube(self):
        self.assertEqual(client.start('https://www.youtube.com/', 'GET', 300, '0').status_code, 200)
    
    def test_cookies(self):
        self.assertGreater(len(client.start('https://www.youtube.com/', 'GET', 300, '0').cookies), 0)

if __name__ == "__main__":
    unittest.main()
