import client
import argparse

parser = argparse.ArgumentParser(description='https-client')
parser.add_argument('url', type=str,
                    help='Фраза для поиска')

parser.add_argument('method', type=str, choices=['GET', 'POST', 'HEAD', 'OPTIONS'],
                    help='GET|POST|HEAD|OPTIONS')

parser.add_argument('-t', dest='timeout', type=str, default='5',
                    help='Время ожидания')

parser.add_argument('-s', dest='save', type=str, default=None,
                    help='Сохранение в файл для GET или данные для POST через _')

parser.add_argument('-d', dest='data', type=str, default=None,
                    help='Данные для отправки')
args = parser.parse_args()

if __name__ == "__main__":
    client.start(args.url, args.method, int(args.timeout), args.save, args.data)
