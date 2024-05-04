import tkinter


def is_intersect(rect1, rect2):
    return rect1[2] >= rect2[0] and rect1[0] <= rect2[2] and rect1[3] >= rect2[1] and rect1[3] <= rect2[3]


class Ball:
    def __init__(self, canvas, paddle, blocks, speed, size=15, color='red'):
        self.canvas, self.blocks = canvas, blocks
        self.paddle, self.speed = paddle, speed
        self.x, self.y = 0, -self.speed
        self.id = canvas.create_oval(10, 10, size, size, fill=color)
        self.canvas.move(self.id, 245, 200)

    def hit_block(self, pos):
        for block in self.blocks:
            if is_intersect(pos, self.canvas.coords(block)):
                self.canvas.delete(block)
                self.blocks.remove(block)
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0 or self.hit_block(pos):
            self.y = self.speed
        if pos[3] >= self.canvas.winfo_height():
            self.y = -self.speed
        if pos[0] <= 0 or self.hit_block(pos):
            self.x = self.speed
        if pos[2] >= self.canvas.winfo_width():
            self.x = -self.speed
        if is_intersect(pos, self.canvas.coords(self.paddle.id)):
            self.y = -self.speed
            if self.paddle.direction == 'left':
                self.x = -self.speed
            elif self.paddle.direction == 'right':
                self.x = self.speed


class Paddle:
    def __init__(self, canvas, speed, width=100, height=10, color='blue'):
        self.canvas, self.speed = canvas, speed
        self.id = canvas.create_rectangle(0, 0, width, height, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x, self.direction = 0, None
        self.canvas.bind_all('<KeyPress-Left>', self.move_left)
        self.canvas.bind_all('<KeyPress-Right>', self.move_right)
        self.canvas.bind_all('<KeyRelease-Left>', self.stop)
        self.canvas.bind_all('<KeyRelease-Right>', self.stop)

    def draw(self):
        pos = self.canvas.coords(self.id)
        if pos[0] + self.x >= 0 and pos[2] + self.x <= self.canvas.winfo_width():
            self.canvas.move(self.id, self.x, 0)
        else:
            self.x = 0

    def move_left(self, _):
        self.x = -self.speed
        self.direction = 'left'

    def move_right(self, _):
        self.x = self.speed
        self.direction = 'right'

    def stop(self, _):
        self.x = 0
        self.direction = None


class Breakout(tkinter.Tk):
    def __init__(self, speed=2):
        super().__init__()
        self.title('Breakout Game | By ruzhila.cn')
        self.canvas = tkinter.Canvas(self, width=500, height=400, bd=0)
        self.canvas.pack()
        self.blocks = [self.create_block(x * 60, y * 20)
                       for x in range(8) for y in range(4)]
        self.paddle = Paddle(self.canvas, speed * 1.5)
        self.ball = Ball(self.canvas, self.paddle, self.blocks, speed)
        self.after(10, self.loop)

    def create_block(self, x, y, fill='green'):
        block = self.canvas.create_rectangle(0, 0, 60, 20, fill=fill)
        self.canvas.move(block, x, y)
        return block

    def loop(self):
        if len(self.blocks) == 0:
            return
        self.ball.draw()
        self.paddle.draw()
        self.after(10, self.loop)


if __name__ == '__main__':
    Breakout().mainloop()
