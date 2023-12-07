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

    def post(self, url, timeout, data):
        port = self.__get_port(url)
        host = urlparse(url).hostname
        path = self.__get_path(url)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        response = pickle.dumps(data)
        sock.connect((host, port))
        if port == 443:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=host)
        sock.sendall(f"POST {path} HTTP/1.1\r\nHost:{host}\r\n\r\n{response}".encode())
        sock.settimeout(timeout)
        result = sock.recv(1024)
        if result:
            self.status_code = self.__get_status_code(result)
        return int(self.status_code)

    def get(self, url, timeout):
        port = self.__get_port(url)
        host = urlparse(url).hostname
        path = self.__get_path(url)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        response = b""
        try:
            sock.connect((host, port))
            if port == 443:
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)
            sock.sendall(f"GET {path} HTTP/1.1\r\nHost:{host}\r\n\r\n".encode())
            sock.settimeout(timeout)
            while True:
                data = sock.recv(1024)
                response += data
                if b'\r\n0\r\n\r\n' in data:
                    break
                elif b'\r\n\r\n' in data:
                    break
                elif not data:
                    break
            if response:
                self.status_code = self.__get_status_code(response)
                self.headers = self.__get_headers(response)
                self.content = self.__get_content(port, response)
                self.text = self.__get_text(port, response)
                self.cookies = self.get_cookies(self.headers)
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
        return headers['Set-Cookie']

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


def start(url, method, timeout, more):
    req = SockGet()
    if method == 'GET':
        ex = req.get(url=url, timeout=timeout)
        if ex:
            print(f"Error: {ex}")
            #sys.exit(0)
        if req.status_code == 200:
            print(req.status_code)
            print(req.headers)
            if more == '1':
                save_in_file(url, req.headers)
        else:
            print(f"Status Code: {req.status_code}")
        return req
    elif method == 'POST':
        data = dict()
        more = more.split('+')
        for i in more:
            g = i.split('_')
            key = g[0]
            value = g[1:]
            data[key] = value
        req.post(url=url, timeout=timeout, data=data)
        if req.status_code == 200:
            print(req.status_code)
        else:
            print(f"Status Code: {req.status_code}")
            #sys.exit(0)
        return req
    else:
        raise Exception('Неверный метод')


def save_in_file(url, data):
    name = url[url.find('//')+2: url.rfind('/')] + '.txt'
    my_file = open(name, "w+")
    for key, value in data.items():
        my_file.write(str(key) + ': ' + str(value) + '\n')
    my_file.writelines(data)


def main():
    pass



if __name__ == "__main__":
    main()
