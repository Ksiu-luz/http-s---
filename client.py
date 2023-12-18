import socket
import ssl
import sys
import pickle
from urllib.parse import urlparse


class SockGet:
    def __init__(self):
        self.status_code = None
        self.headers = None
        self.content = None
        self.text = None
        self.cookies = None

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

    def method(self, method, url, timeout, data):
        port = self.__get_port(url)
        host = urlparse(url).hostname
        path = self.__get_path(url)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        encode_data = ''
        if data is not None:
            encode_data = pickle.dumps(data)
        response = b""
        try:
            sock.connect((host, port))
            if port == 443:
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)
            sock.sendall(f"{method} {path} HTTP/1.1\r\nHost:{host}\r\n\r\n{encode_data}".encode())
            sock.settimeout(timeout)
            while True:
                data = sock.recv(1024)
                response += data
                if b'\r\n0\r\n\r\n' in data or b'\r\n\r\n' in data or not data:
                    break
            if response:
                self.status_code = self.__get_status_code(response)
                self.headers = self.__get_headers(response)
                self.content = self.__get_content(port, response)
                self.text = self.__get_text(port, response)
                self.cookies = self.get_cookies(self.headers)
                if self.status_code == 301:
                    print('Status Code: 301')
                    return self.method('GET', self.headers['Location'], timeout, data)
            sock.close()
            return int(self.status_code), self.headers, self.content
        except Exception as ex:
            sock.close()
            return ex

    @staticmethod
    def __get_status_code(response):
        return int(response.decode().split('\r\n\r\n')[0].splitlines()[0].split()[1:-1][0])
    
    @staticmethod
    def get_cookies(headers):
        try:
            cookie = headers['Set-Cookie']
        except:
            cookie = None
        return cookie

    @staticmethod
    def __get_headers(response):
        headers = dict()
        for head in response.decode().split('\r\n\r\n')[0].splitlines()[1:]:
            headers.update({head.split(": ")[0]: head.split(": ")[1]})
        return headers

    @staticmethod
    def __get_content(port, response):
        if port == 80:
            return response.decode().split('\r\n\r\n')[1].split("\r\n")[1].encode()
        return response.decode().split('\r\n\r\n')[1].encode()

    @staticmethod
    def __get_text(port, response):
        if port == 80:
            return response.decode().split('\r\n\r\n')[1].split("\r\n")[1]
        return response.decode().split('\r\n\r\n')[1]


def start(url, method, timeout, save, data):
    req = SockGet()
    req.method(method, url=url, timeout=timeout, data=data)
    if req.status_code == 200:
        print(req.status_code)
        print(req.headers)
        if save:
            save_in_file(req.headers, save)
    else:
        print(f"Status Code: {req.status_code}")
    return req


def save_in_file(data, name):
    my_file = open(name, "w+")
    for key, value in data.items():
        my_file.write(str(key) + ': ' + str(value) + '\n')
    my_file.writelines(data)
