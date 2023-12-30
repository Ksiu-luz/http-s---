import client
import argparse

parser = argparse.ArgumentParser(description='https-client')
parser.add_argument('url', type=str,
                    help='Адрес сайта')

parser.add_argument('method', type=str, choices=['GET', 'POST', 'HEAD', 'OPTIONS'],
                    help='GET|POST|HEAD|OPTIONS')

parser.add_argument('-hd', dest='headers', type=str, default=None,
                    help='Заголовки в формате {key1}:{value1}+{key2}:{value2}')

parser.add_argument('-t', dest='timeout', type=str, default='5',
                    help='Время ожидания ответа')

parser.add_argument('-s', dest='save', type=str, default=None,
                    help='Имя файла для сохранение ответа')

parser.add_argument('-d', dest='data', type=str, default=None,
                    help='Тело запроса в формате {key1}:{value1}+{key2}:{value2}')

parser.add_argument('-c', dest='use_cookies', type=str, default=None)

args = parser.parse_args()

if __name__ == "__main__":
    cl, cookie = client.start(url=args.url,
                              method=args.method,
                              headers=args.headers,
                              timeout=int(args.timeout),
                              save=args.save,
                              data=args.data,
                              use_cookies=args.use_cookies)
    if args.use_cookies:
        print(f'Данные Cookie: {cookie}')
