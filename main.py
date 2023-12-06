import client
import argparse

parser = argparse.ArgumentParser(description='https-client')
parser.add_argument('url', type=str, help='Фраза для поиска')
parser.add_argument('method', type=str, help='GET|POST')
parser.add_argument('timeout', type=str, help='Время ожидания')
parser.add_argument('more', type=str, help='Сохранение в файл для GET или данные для POST через _')
args = parser.parse_args()

if __name__ == "__main__":
    client.start(args.url, args.method, int(args.timeout), args.more)