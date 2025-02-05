import tkinter
import tkinter.font
import conf
from layout import Layout
from browser import URL
from utils.lex import lex


class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=conf.WIDTH,
            height=conf.HEIGHT,
        )
        self.canvas.pack()
        self.display_list = []
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<MouseWheel>", self.scroll_with_wheel)
        self.display_list = []

    def scrolldown(self, e):
        self.scroll += conf.SCROLL_STEP
        self.draw()

    def scroll_with_wheel(self, e):
        """Обработка прокрутки колесиком мыши"""
        if e.delta > 0:
            self.scroll -= conf.SCROLL_STEP  # Прокрутка вверх
        else:
            self.scroll += conf.SCROLL_STEP  # Прокрутка вниз
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, word, font in self.display_list:
            if y > self.scroll + conf.HEIGHT:
                continue
            if y + font.metrics("linespace") < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=word, font=font, anchor="nw")

    def load(self, url):
        body = url.request()
        tokens = lex(body)
        self.display_list = Layout(tokens).display_list
        self.draw()


if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
