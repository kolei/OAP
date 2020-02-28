[содержание](/readme.md)  

# HTTP-клиент

В стандартной библиотеке Python есть ряд готовых модулей по работе с HTTP.

* urllib
* httplib

Если уж совсем хочется хардкора, то можно и сразу с *socket* поработать. Но у всех этих модулей есть один большой недостаток - неудобство работы.

Во-первых, большое обилие классов и функций. Во-вторых, код получается вовсе не pythonic. Многие программисты любят Python за его элегантность и простоту, поэтому и был создан модуль, призванный решать проблему существующих и имя ему **requests** или [HTTP For Humans](http://docs.python-requests.org/en/master/).

* [Обработка исключений в requests](#Обработка-исключений-в-requests)
* [Быстрый старт](#Быстрый-старт)
    * [Простые запросы](#Простые-запросы)
    * [Передача параметров в GET-запросе](#Передача-параметров-в-GET-запросе)
    * [Содержимое ответа сервера (content)](#Содержимое-ответа-сервера-(content))
    * [JSON](#JSON)
    * [Настраиваемые заголовки](#Настраиваемые-заголовки)
    * [Подробнее о POST-запросах](#Подробнее-о-POST-запросах)
    * [Код ответа](#Код-ответа)
    * [Заголовки ответа](#Заголовки-ответа)
    * [Cookies](#Плюшки-(Cookies))
    * [Timeout](#Timeout-(время-ожидания))
* [Авторизация](#Авторизация)
    * [Базовая авторизация (Basic Authentication)](#Базовая-авторизация-(Basic-Authentication))
    * [Авторизация с подписью (Digest Authentication)](#Авторизация-с-подписью-(Digest-Authentication))


## Что же умеет requests?

Для начала хочется показать как выглядит код работы с http, используя модули из стандартной библиотеки Python и код при работе с requests. В качестве мишени для стрельбы http запросами будет использоваться очень удобный сервис httpbin.org

```py
import urllib.request
response = urllib.request.urlopen('https://httpbin.org/get')
print(response.read())
print(response.getheader('Server'))
print(response.getcode())
```

В консоли будет примерно такое:

```
'{\n  "args": {}, \n  "headers": {\n    "Accept-Encoding": "identity", \n    "Host": "httpbin.org", \n    "User-Agent": "Python-urllib/3.5"\n  }, \n  "origin": "95.56.82.136", \n  "url": "https://httpbin.org/get"\n}\n'
nginx
200
```

Кстати, urllib.request это надстройка над "низкоуровневой" библиотекой httplib.

Теперь попробуем выполнить то же самое с помощью **requests**

```py
import requests
response = requests.get('https://httpbin.org/get')
print(response.content)
print(response.json())
print(response.headers)
print(response.headers.get('Server'))
```

В консоли будет что-то типа:

```
b'{\n  "args": {}, \n  "headers": {\n    "Accept": "*/*", \n    "Accept-Encoding": "gzip, deflate", \n    "Host": "httpbin.org", \n    "User-Agent": "python-requests/2.9.1"\n  }, \n  "origin": "95.56.82.136", \n  "url": "https://httpbin.org/get"\n}\n'

{'headers': {'Accept-Encoding': 'gzip, deflate', 'User-Agent': 'python-requests/2.9.1', 'Host': 'httpbin.org', 'Accept': '*/*'}, 'args': {}, 'origin': '95.56.82.136', 'url': 'https://httpbin.org/get'}

{'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Server': 'nginx', 'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': '*', 'Content-Length': '237', 'Date': 'Wed, 23 Dec 2015 17:56:46 GMT'}

nginx
```

В простых методах запросов значительных отличий у них не имеется. Но давайте взглянем на работу с Basic Auth:

Стандартная библиотека:

'''py
import urllib.request
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
top_level_url = 'https://httpbin.org/basic-auth/user/passwd'
password_mgr.add_password(None, top_level_url, 'user', 'passwd')
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)
response = opener.open(top_level_url)
response.getcode()
# 200
response.read()
# b'{\n  "authenticated": true, \n  "user": "user"\n}\n'
```

requests:

```py
import requests
response = requests.get('https://httpbin.org/basic-auth/user/passwd', auth=('user', 'passwd'))
print(response.content)
# b'{\n  "authenticated": true, \n  "user": "user"\n}\n'
print(response.json())
# {'user': 'user', 'authenticated': True}
```

Разница на лицо. И несмотря на тот факт, что **requests** ничто иное как обёртка над urllib3, а последняя является надстройкой над стандартными средствами Python, удобство написания кода в большинстве случаев является приоритетом номер один.

В requests имеется:

* Множество методов http аутентификации
* Сессии с куками
* Полноценная поддержка SSL
* Различные методы-плюшки вроде .json(), которые вернут данные в нужном формате
* Проксирование
* Грамотная и логичная работа с исключениями

О последнем пункте хотелось бы поговорить чуточку подробнее.

## Обработка исключений в requests

**При работе с внешними сервисами никогда не стоит полагаться на их отказоустойчивость**. Всё упадёт рано или поздно, поэтому нам, программистам, необходимо быть всегда к этому готовыми, желательно заранее и в спокойной обстановке.

Итак, как у requests дела обстоят с различными ошибками в момент сетевых соединений? Для начала определим ряд проблем, которые могут возникнуть:

* Хост недоступен. Обычно такого рода ошибка происходит из-за проблем конфигурирования DNS. (DNS lookup failure)
* "Вылет" соединения по таймауту
* Ошибки HTTP. Подробнее о HTTP кодах можно посмотреть [здесь](https://www.restapitutorial.com/httpstatuscodes.html).
* Ошибки SSL соединений (обычно при наличии проблем с SSL сертификатом: просрочен, не является доверенным и т.д.)

Базовым классом-исключением в requests является **RequestException**. От него наследуются все остальные

* HTTPError
* ConnectionError
* Timeout
* SSLError
* ProxyError

И так далее. Полный список всех исключений можно посмотреть в requests.exceptions.

### Timeout

В requests имеется 2 вида таймаут-исключений:

* **ConnectTimeout** - таймаут на соединения
* **ReadTimeout** - таймаут на чтение

```py
import requests

try:
    response = requests.get('https://httpbin.org/user-agent', 
                            timeout=(0.00001, 10))
except requests.exceptions.ConnectTimeout:
    print('Oops. Connection timeout occured!')

# Oops. Connection timeout occured!

try:
    response = requests.get('https://httpbin.org/user-agent', 
                            timeout=(10, 0.0001))
except requests.exceptions.ReadTimeout:
    print('Oops. Read timeout occured')
except requests.exceptions.ConnectTimeout:
    print('Oops. Connection timeout occured!')

# Oops. Read timeout occured
```

### ConnectionError

```py
import requests

try:
    response = requests.get('http://urldoesnotexistforsure.bom')
except requests.exceptions.ConnectionError:
    print('Seems like dns lookup failed..')
     
# Seems like dns lookup failed..
```

### HTTPError

```py
import requests

try:
    response = requests.get('https://httpbin.org/status/500')
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print('Oops. HTTP Error occured')
    print('Response is: {content}'.format(content=err.response.content))
     
# Oops. HTTP Error occured
# Response is: b''
```

Я перечислил основные виды исключений, которые покрывают, пожалуй, 90% всех проблем, возникающих при работе с http. Главное помнить, что если мы действительно намерены отловить что-то и обработать, то это необходимо явно запрограммировать, если же нам неважен тип конкретного исключения, то можно отлавливать общий базовый класс RequestException и действовать уже от конкретного случая, например, залоггировать исключение и выкинуть его дальше наверх. 


## Быстрый старт

### Простые запросы

```py
import requests

# обычный GET
r = requests.get('https://api.github.com/events')

# POST, в параметре data передается словарь
r = requests.post('https://httpbin.org/post', data = {'key':'value'})

# поддерживаются дополнительные методы, позволяющие организовать запросы к REST-серверу
r = requests.put('https://httpbin.org/put', data = {'key':'value'})
r = requests.delete('https://httpbin.org/delete')
r = requests.head('https://httpbin.org/get')
r = requests.options('https://httpbin.org/get')
```

### Передача параметров в GET-запросе

Как послать POST запрос выше уже показано, а как насчет GET?

```py
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get('https://httpbin.org/get', params=payload)

# можно посмотреть на получившийся URL:
print(r.url)

# https://httpbin.org/get?key2=value2&key1=value1
```

### Содержимое ответа сервера (content)

```py
import requests

r = requests.get('https://api.github.com/events')
print(r.text)
# '[{"id": "9140873463","type": "CreateEvent","actor":{...'
```

Строка, как и положено Питону, в UTF-8. Оригинальную кодировку (которая указана в HTTP-заголовке) можно посмотреть в аттрибуте ``r.encoding``

### JSON

Если в ответе сервера ожидается JSON, то можно просто вызвать встроенный метод ``.json()`` для получения словаря.

```py
import requests

r = requests.get('https://api.github.com/events')
print(r.json())
# [{"id": "9140873463","type": "CreateEvent","actor":{...
```

### Настраиваемые заголовки

Если нужно изменить стандарные заголовки или добавить свой, то используйте параметр *headers* 

```py
url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}
r = requests.get(url, headers=headers)
```

### Подробнее о POST-запросах

Если нужно послать данные в формате ``form-encoded``, то достаточно  параметру data присвоить словарь или кортеж. 

```py
#обычный запрос, в data передается словарь 
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post("https://httpbin.org/post", data=payload)

# в data передается кортеж 
payload_tuples = [('key1', 'value1'), ('key1', 'value2')]
r1 = requests.post('https://httpbin.org/post', data=payload_tuples)

# в data передается словарь с массивом в значении ключа 
payload_dict = {'key1': ['value1', 'value2']}
r2 = requests.post('https://httpbin.org/post', data=payload_dict)
```

Если же нужно послать не в ``form-encoded`` формате, то нужно либо присвоить параметру data строку:

```py
import json

payload = {'some': 'data'}

r = requests.post('https://api.github.com/some/endpoint', data=json.dumps(payload))
```

Либо вместо *data* использовать параметр *json*:

```py
payload = {'some': 'data'}
r = requests.post(url, json=payload)
```

>параметр *json* будет проигнорирован, если одновременно задать параметр *data* или *files*

### Код ответа

```py
r = requests.get('https://httpbin.org/get')
r.status_code # 200
```

### Заголовки ответа

Ответы хранятся в словаре *headers*

```py
r.headers
# {
#     'content-encoding': 'gzip',
#     'transfer-encoding': 'chunked',
#     'connection': 'close',
#     'server': 'nginx/1.0.4',
#     'x-runtime': '148ms',
#     'etag': '"e1ca502697e5c9317743dc078f67693f"',
#     'content-type': 'application/json'
# }
```

Словарь специальный, т.к. HTTP-заголовки должны быть регистро независимыми. Обратиться к элементу словаря можно используя любой регистр:

```py
r.headers['Content-Type']
# 'application/json'

r.headers.get('content-type')
# 'application/json'
```

### Плюшки (Cookies)

```py
r = requests.get(url)

#вытаскивает из ответа куку по имени
r.cookies['example_cookie_name']
```

Для отправки куки вместе с запросом используйте параметр *cookies*:

```py
cookies = dict(cookies_are='working')

r = requests.get(url, cookies=cookies)
```

Есть и более продвинутые способы работы с куками:

```py
jar = requests.cookies.RequestsCookieJar()
jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
r = requests.get(url, cookies=jar)
r.text #'{"cookies": {"tasty_cookie": "yum"}}'
```

### Timeout (время ожидания)

Желательно задавать время ожидания запроса, т.к. значение по-умолчанию может быть достаточно большим. Время задается в секундах.

Можно задать таймаут как на соединение в целом, так и выделить таймаут на чтение отдельно

```py
# общий таймаут
r = requests.get('https://github.com', timeout=5)
# таймаут на соединение 3 сек, таймаут на чтение 27 сек 
r = requests.get('https://github.com', timeout=(3.05, 27))
```

## Авторизация

Большинство веб-сервисов требуют авторизацию, причем вариантов авторизации достаточно много. Requests поддерживает некоторые из них, от простых до достаточно сложных:

### Базовая авторизация (Basic Authentication)

Это самый простой способ авторизации, при котором данные для авторизации передаются в заголовоке HTTP-запроса.
>Данные просто "упакованы" в base64, поэтому такой способ можно использовать только при обмене через защищенное соединение (HTTPS)

```py
import requests
requests.get('https://api.github.com/user', 
             auth=requests.auth.HTTPBasicAuth('user', 'pass'))

# то же самое можно сделать и проще, requests сам применит базовую авторизацию, если тип явно не указан
requests.get('https://api.github.com/user', auth=('user', 'pass'))
```

### Авторизация с подписью (Digest Authentication)

**Digest Authentication** — один из общепринятых методов, используемых веб-сервером для обработки учетных данных пользователя веб-браузера. Аналогичный метод используется в рамках VoIP-протокола SIP для аутентификации сервером обращения со стороны клиента, т.е. оконечного терминала. Данный метод отправляет по сети хеш-сумму логина, пароля, адреса сервера и случайных данных, и предоставляет больший уровень защиты, чем базовая аутентификация, при которой данные отправляются в открытом виде.

Технически, аутентификация по дайджесту представляет собой применение криптографической хеш-функции MD5 к секрету пользователя с использованием случайных значений для затруднения криптоанализа и предотвращения replay-атак.

```py
import requests
...
requests.get(url, auth=requests.auth.HTTPDigestAuth('user', 'pass'))
```

[содержание](/readme.md)  