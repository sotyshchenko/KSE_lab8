import pgzrun

HEART_RADIUS = 20

# Ball class
class Ball:
    def __init__(self, pos=(200,300), vel=(2, -2)):
        self.pos = list(pos)
        self.vel = list(vel)
        self.radius = 5

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        for obstacle in obstacles:
            if touch(self, obstacle):
                obstacles.remove(obstacle)
                self.vel[1] = -self.vel[1]

    def draw(self):
        screen.draw.filled_circle(self.pos, self.radius, 'black')

# Obstacle class
class Obstacle:
    def __init__(self, pos=(100,100), radius=20):
        self.pos = list(pos)
        self.radius = radius

    def draw(self):
        screen.draw.filled_circle(self.pos, self.radius, 'blue')

# Paddle class
class Paddle:
    def __init__(self, pos=(200,400), size=(50, 10)):
        self.pos = list(pos)
        self.size = list(size)

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        self.pos[0] = mouse_pos[0]

    def draw(self):
        screen.draw.filled_rect(self.pos+self.size, 'red')

# Touch function to check for collision between ball and obstacles
def touch(ball, obstacle):
    dx = ball.pos[0]-obstacle.pos[0]
    dy = ball.pos[1]-obstacle.pos[1]
    distance = (dx*dx + dy*dy)**0.5
    return distance <= ball.radius + obstacle.radius

# Global Variables
lives = 3
ball = Ball()
obstacles = []
num_obstacles = 6
paddle = Paddle()

# Generate Obstacles
for i in range(num_obstacles):
    x_pos = pg.width/2 - 50 + i*50
    y_pos = 50
    obstacle = Obstacle((x_pos, y_pos))
    obstacles.append(obstacle)

def draw():
    screen.fill('white')
    paddle.draw()
    ball.draw()
    for obstacle in obstacles:
        obstacle.draw()
    for i in range(lives):
        x_pos = 20 + i*HEART_RADIUS*2
        screen.draw.filled_circle((x_pos,HEART_RADIUS),HEART_RADIUS, 'pink')

def update():
    ball.update()
    paddle.update()

def on_mouse_move(pos):
    paddle.update()

# Game Control
def on_frame():
    if ball.pos[1] > screen.height - ball.radius:
        if ball.pos[0] < paddle.pos[0] or ball.pos[0] > paddle.pos[0] + paddle.size[0]:
            lives -= 1
            ball.pos = [200, 300]
    if lives <= 0:
        game.over = True

pgzrun.go()
