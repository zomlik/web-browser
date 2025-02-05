from layout import Text, Tag


def lex(body):
    """Разбор входной строки на текстовые элементы и теги.

        Эта функция анализирует строку, содержащую HTML разметку,
        и преобразует её в список объектов Text и Tag.

        :param body: Входная строка для анализа.
        :return: Список объектов Text и Tag.
    """
    out = []
    buffer = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if buffer:
                out.append(Text(buffer))
            buffer = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(buffer))
            buffer = ""
        else:
            buffer += c
    if not in_tag:
        out.append(Text(buffer))
    return out
