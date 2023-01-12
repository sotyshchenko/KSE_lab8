import pgzrun
from pgzero.actor import Actor

#from old.vector import Vector


class Paddle:
    def __init__(self):
        pass


class Ball:
    def __init__(self):
        pass


class Obstacle:
    def __init__(self):
        pass


class Hearts:
    def __init__(self):
        self.actor = Actor('heart', center=(10, 10))

    def draw(self):
        self.actor.draw()


WIDTH = 600
HEIGHT = 800

heart = Actor('heart')

heart.pos = 20, 20


def draw():
    screen.clear()
    heart.draw()


def update(dt):
    #paddle
    pass


def on_mouse_move(pos):
    #paddle.
    pass


pgzrun.go()
