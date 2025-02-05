import conf
from utils.get_font import get_font


class Text:
    """Класс для хранения текста"""
    def __init__(self, text):
        self.text = text


class Tag:
    """Класс для хранения тегов"""
    def __init__(self, tag):
        self.tag = tag


class Layout:
    """Класс для управления размещением текста и тегов на экране"""
    def __init__(self, tokens):
        """Инициализация объекта Layout.
            :param tokens: Список токенов (текст и теги) для размещения.
        """
        self.tokens = tokens
        self.display_list = []  # Список для хранения отображаемых элементов

        self.line = []
        self.flush()

        self.cursor_x = conf.H_STEP
        self.cursor_y = conf.V_STEP
        self.weight = "normal"
        self.style = "roman"
        self.size = 12

        for tok in tokens:
            self.token(tok)

    def token(self, tok):
        """Обработка токена (текста или тега)"""
        # Если токен - текст, разбиваем его на слова и обрабатываем каждое слово
        if isinstance(tok, Text):
            for word in tok.text.split():
                self.word(word)
        # Устанавливаем стиль шрифта (курсив, обычный, жирный)
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
        # Устанавливаем размер шрифта
        elif tok.tag == "small":
            self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
        # Перенос строки
        elif tok.tag == "br":
            self.flush()
        # Завершение параграфа: перенос строки и добавление отступа
        elif tok.tag == "/p":
            self.flush()
            self.cursor_y += conf.V_STEP

    def word(self, word):
        """Обработка слова и его размещение на экране"""
        # Создаем шрифт с текущими параметрами
        font = get_font(
            size=self.size,
            weight=self.weight,
            style=self.style
        )
        # Измеряем ширину слова
        w = font.measure(word)
        # Добавляем слово в список отображаемых элементов
        if self.cursor_x + w > conf.WIDTH - conf.H_STEP:
            self.flush()
        self.line.append((self.cursor_x, word, font))
        self.cursor_x += w + font.measure(" ")

    def flush(self):
        """Завершение текущей строки и подготовка к следующей"""
        if not self.line:
            return
        # Получаем метрики шрифтов для всех слов в строке
        metrics = [font.metrics() for x, word, font in self.line]
        # Находим максимальное значение ascent (высота над базовой линией)
        max_ascent = max([metric["ascent"] for metric in metrics])
        # Вычисляем базовую линию для текущей строки
        baseline = self.cursor_y + 1.25 * max_ascent
        # Размещаем каждое слово на экране
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
        # Находим максимальное значение descent (высота под базовой линией)
        max_descent = max([metric["descent"] for metric in metrics])
        # Обновляем позицию курсора по Y
        self.cursor_y = baseline + 1.25 * max_descent
        # Сбрасываем позицию курсора по X
        self.cursor_x = conf.H_STEP
        # Очищаем текущую строку
        self.line = []
