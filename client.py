import socket
import ssl
import sys
import os
from urllib.parse import urlparse, urlencode


class Sock:
    def __init__(self):
        self.status_code = None
        self.headers = None
        self.content = None
        self.text = None
        self.response = b""
        self.cookies = None

    def method(self, url, method, headers, timeout, data, use_cookies=False):
        port = self.__get_port(url)
        host = urlparse(url).hostname
        path = self.__get_path(url)
        self.response = b""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            if port == 443:
                context = ssl.create_default_context()
                s = context.wrap_socket(s, server_hostname=host)
            request = f'{method} {path} HTTP/1.1\r\nHost: {host}'

            if headers is not None:
                heads = ''
                for key, value in headers.items():
                    heads += f'\r\n{key}: {value}'
                request += heads

            if data is not None:
                encoded_data = urlencode(data).encode('utf-8')
                if headers is not None:
                    if use_cookies and self.cookies is not None and 'Cookie' not in headers:
                        request += f"\r\n{self.cookies}"
                    if 'Content-Type' not in headers:
                        request += "\r\nContent-Type: application/x-www-form-urlencoded"
                    if 'Content-Length' not in headers:
                        request += f"\r\nContent-Length: {len(encoded_data)}\r\n\r\n"
                else:
                    request += "\r\nContent-Type: application/x-www-form-urlencoded"
                    request += f"\r\nContent-Length: {len(encoded_data)}\r\n\r\n"
                s.sendall(request.encode('utf-8') + encoded_data)
            else:
                s.sendall(f'{request}\r\n\r\n'.encode('utf-8'))

            # Получаем данные
            while True:
                try:
                    chunk = s.recv(1024)
                except TimeoutError:
                    break
                self.response += chunk
                if method in ('POST', 'HEAD', 'OPTIONS') and b'\r\n\r\n' in self.response:
                    break
                if b'HTTP/1.1 3' in self.response and b'Location' in self.response:
                    break
                if not chunk or b'\r\n0\r\n\r\n' in self.response:
                    break

            if self.response:
                self.status_code = self.__get_status_code(self.response)
                self.headers = self.__get_headers(self.response)
                if 400 > self.status_code[0] >= 300:
                    print(self.status_code[0], self.status_code[1])
                    print('Выполняется перенаправление...')
                    return self.method(self.headers['Location'], method, headers, timeout, data, use_cookies)
                if use_cookies:
                    self.__update_cookies()
                self.content = self.__get_content(self.response, port)
                self.text = self.__get_text(self.response, port)
                print(self.status_code[0], self.status_code[1])
        return self.status_code, self.headers, self.text

    @staticmethod
    def __get_port(url):
        if ":" in urlparse(url).netloc:
            return int(str(urlparse(url).netloc).split(":")[-1])
        elif urlparse(url).scheme == "http":
            return 80
        else:
            return 443

    @staticmethod
    def __get_path(url):
        if not urlparse(url).path:
            return "/"
        else:
            if "?" in url:
                key = f'?{url.split("?")[-1]}'
                return f'{urlparse(url).path}{key}'
            else:
                return urlparse(url).path

    @staticmethod
    def __decode(data):
        try:
            return data.decode()
        except UnicodeDecodeError:
            return data.decode('windows-1251')

    def __update_cookies(self):
        try:
            self.cookies = self.headers['Set-Cookie']
            print('Cookie обновлены')
        except KeyError:
            self.cookies = None
            print('Cookie отсутствуют')

    def __get_status_code(self, response):
        try:
            raw_data = self.__decode(response).split('\r\n')[0].split(' ')[1:]
            status = int(raw_data[0])
            info = ' '.join(raw_data[1:])
        except UnicodeDecodeError:
            sys.exit('Данные ответа были повреждены. Декодирование невозможно.')

        return status, info

    def __get_headers(self, response):
        raw_data = self.__decode(response).split('\r\n\r\n')[0].split('\r\n')[1:]
        headers = dict()
        for head in raw_data:
            spam = head.split(': ')
            headers[spam[0]] = ': '.join(spam[1:])
        return headers

    def __get_content(self, response, port):
        raw_data = self.__decode(response)
        if port == 80:
            return raw_data.split('\r\n\r\n')[1].split("\r\n")[1].encode()
        return raw_data.split('\r\n\r\n')[1].encode()

    def __get_text(self, response, port):
        raw_data = self.__decode(response)
        if port == 80:
            return raw_data.split('\r\n\r\n')[1].split("\r\n")[1]
        return raw_data.split('\r\n\r\n')[1]

    def save(self, filename):
        os.chdir("tests")
        with open(f"{filename}.txt", 'w+', encoding='utf-8') as f:
            f.write(self.__decode(self.response))


def start(url, method, headers, timeout, save, data, use_cookies=False):
    req = Sock()
    try:
        if headers is not None:
            temp_headers = {}
            spam = headers.split('+')
            for line in spam:
                key, value = line.split(':')
                temp_headers[key] = value
            headers = temp_headers
    except Exception:
        sys.exit('Неверный формат заголовков')

    try:
        if data is not None:
            temp_data = {}
            spam = data.split('+')
            for line in spam:
                key, value = line.split(':')
                temp_data[key] = value
            data = temp_data
    except Exception:
        sys.exit('Неверный формат тела запроса')

    req.method(method=method, url=url, headers=headers, timeout=timeout, data=data, use_cookies=use_cookies)
    if save is not None:
        req.save(save)
    return req, req.cookies


if __name__ == '__main__':
    pass
