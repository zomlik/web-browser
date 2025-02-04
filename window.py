import tkinter
from browser import URL


class Browser:
    WIDTH, HEIGHT = 800, 600
    HSTEP, VSTEP = 13, 18
    SCROLL_STEP = 100

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.WIDTH,
            height=self.HEIGHT,
        )
        self.canvas.pack()
        self.text = ""
        self.display_list = []
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)

    def scrolldown(self, e):
        self.scroll += self.SCROLL_STEP
        self.draw()

    def lex(self, body):
        in_tag = False
        for c in body:
            if c == "<":
                in_tag = True
            elif c == ">":
                in_tag = False
            elif not in_tag:
                self.text += c
        return self.text

    def layout(self):
        cursor_x, cursor_y = self.HSTEP, self.VSTEP
        for c in self.text:
            self.display_list.append((cursor_x, cursor_y, c))
            cursor_x += self.HSTEP
            if cursor_x >= self.WIDTH:
                cursor_y += self.VSTEP
                cursor_x = self.HSTEP

        return self.display_list

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + self.HEIGHT:continue
            if y + self.VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c)

    def load(self, url):
        body = url.request()
        self.lex(body)
        self.display_list = self.layout()
        self.draw()

if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()