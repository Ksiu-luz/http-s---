# https-client

Программа предназначена для работы с https

## Установка

Для работы программы необходим Python версии 3 и выше.
Скачайте программу из репозитория.

## Использование

- Для отправки данных введите в консоли: `python main.py {link} POST {options}`
- Для получения данных введите в консоли: `python main.py {link} GET {options}`
- Для получения достпных опций сервера `python main.py {link} OPTIONS {options}`
- Проверка работоспособности сервера `python main.py {link} HEAD {options}`

`{link}` - ссылка на страницу
`{options}` - опции через пробел:
{timeout} - время ожидания
{data} - заголовок и значения через пробел
{headers} - заголовки и значения (для разделения заголовков введите "+")
{save} - название файла для сохранения данных
{use_cookies} - заголовки и значения (для разделения заголовков введите "+")

Пример GET запроса с сохранением в файл:
`python main.py https://ya.ru/ GET -t 300 -s yandex_file`
Пример POST запроса с сохранением в файл:
`python main.py https://ya.ru/ POST -t 300 -s ya_post -d "Data:null"`
Пример HEAD запроса с сохранением в файл:
`python main.py https://ya.ru/ HEAD -t 300 -s ya_head`
Пример OPTIONS запроса с сохранением в файл:
`python main.py https://ya.ru/ OPTIONS -t 300 -s ya_optinos`