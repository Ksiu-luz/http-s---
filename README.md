# https-client

Программа предназначена для работы с https

## Установка

Для работы программы необходим Python версии 3 и выше.
Скачайте программу из репозитория.

## Использование

- Для отправки данных введите в консоли: `python main.py {link} POST {timeout} {data}`
- Для отправки данных введите в консоли: `python main.py {link} GET {timeout} {save}`
- Для возврата состояния сервера `python main.py {link} OPTIONS {timeout} {save}`
- Проверка работоспособности сервера `python main.py {link} HEAD {timeout} {save}`

{link} - ссылка на страницу
{timeout} - время ожидания
{data} - заголовок и значения через пробелы (для разделения заголовков введите "_")

Пример GET запроса с сохранением в файл:
`python main.py https://ya.ru/ GET 300 1`
`python main.py https://youtube.com/ GET 300 1`
Пример POST запроса с сохранением в файл:
`python main.py https://ya.ru/ POST 300 name_nastya_bob+age_5_99`
`python main.py https://translate.yandex.ru/ POST 300 name_nastya_bob+age_5_99`
Пример OPTIONS запроса с сохранением в файл:
`python main.py https://ya.ru/ OPTIONS 300 1`
`python main.py https://youtube.com/ OPTIONS 300 1`
Пример HEAD запроса с сохранением в файл:
`python main.py https://ya.ru/ HEAD 300 1`
`python main.py https://www.youtube.com/ HEAD 300 1`