import conf
import tkinter


def get_font(size, weight, style):
    """Получение шрифта с заданными параметрами.

        Функция ищет шрифт с указанными размером, весом и стилем в кэше.
         Если такой шрифт еще не был создан, он создается и сохраняется в кэш.

        :param size: Размер шрифта.
        :param weight: Вес шрифта ('normal' или 'bold').
        :param style: Стиль шрифта ('roman' или 'italic').
        :return: Объект шрифта Tkinter.
        """
    key = (size, weight, style)
    # Проверка наличия шрифта в кэше
    if key not in conf.FONTS:
        # Создание нового шрифта
        font = tkinter.font.Font(
            size=size,
            weight=weight,
            slant=style
        )
        # Создание временной метки для измерения ширины символов
        label = tkinter.Label(font=font)
        # Сохранение шрифта и метки в кэш
        conf.FONTS[key] = (font, label)
    # Возвращение шрифта из кэша
    return conf.FONTS[key][0]
