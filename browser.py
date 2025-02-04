import socket
import ssl


class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)

        assert self.scheme in ["http", "https"]
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443

        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url

        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def request(self):
        # Создаем сокет для TCP-соединения
        s = socket.socket(
            family=socket.AF_INET,  # Используем IPv4
            type=socket.SOCK_STREAM,  # Тип сокета — потоковый (TCP)
            proto=socket.IPPROTO_TCP,  # Протокол — TCP
        )

        # Подключаемся к серверу на порту 80 или 443
        s.connect((self.host, self.port))

        # Проверяем, используется ли схема"https"
        if self.scheme == "https":
            # Создаем контекст SSL по умолчанию для безопасного соединения
            ctx = ssl.create_default_context()

            # Оборачиваем существующий сокет в SSL-сокет, чтобы обеспечить шифрование
            s = ctx.wrap_socket(s, server_hostname=self.host)

        # Формируем HTTP-запрос методом GET
        request = "GET {} HTTP/1.0\r\n".format(self.path)  # Указываем путь и версию HTTP
        request += "Host: {}\r\n".format(self.host)  # Указываем хост
        request += "\r\n"  # Завершаем заголовки пустой строкой

        # Отправляем запрос на сервер, кодируя его в UTF-8
        s.send(request.encode("utf8"))

        # Создаем файловый объект для чтения ответа от сервера
        response = s.makefile("r", encoding="utf8", newline="\r\n")

        # Читаем первую строку ответа (статусную строку)
        statusline = response.readline()
        # Разделяем статусную строку на версию HTTP, код статуса и пояснение
        version, status, explanation = statusline.split(" ", 2)

        # Создаем словарь для хранения заголовков ответа
        response_headers = {}
        while True:
            line = response.readline()  # Читаем заголовки по одной строке
            if line == "\r\n":  # Пустая строка означает конец заголовков
                break
            # Разделяем строку на имя заголовка и его значение
            header, value = line.split(":", 1)
            # Сохраняем заголовок в словаре (в нижнем регистре для удобства)
            response_headers[header.casefold()] = value.split()

        # Проверяем, что ответ не содержит Transfer-Encoding и Content-Encoding
        # Это важно для упрощения обработки ответа
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        # Читаем тело ответа (содержимое страницы)
        content = response.read()

        # Закрываем сокет
        s.close()

        # Возвращаем содержимое ответа
        return content

    @staticmethod
    def show(body):
        in_tag = False
        for c in body:
            if c == "<":
                in_tag = True
            elif c == ">":
                in_tag = False
            elif not in_tag:
                print(c, end="")


    def load(url):
        body = url.request()
        URL.show(body)

if __name__ == "__main__":
    import sys
    URL.load(URL(sys.argv[1]))