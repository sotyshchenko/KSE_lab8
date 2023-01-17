import pgzrun
import pygame
# # Position ball at the center of the screen.
# ball.pos = (WIDTH/2, HEIGHT/2)
# # Position paddle at the bottom of the screen.
# paddle.pos = (WIDTH/2, HEIGHT - paddle.height)
# # Position obstacle randomly on the top of the screen.
# obstacle.pos = (random.randint(0,WIDTH), 0)
WIDTH = 600
HEIGHT = 800
HEART_RADIUS = 20
global lives
lives = 3
obstacles = []
num_obstacles = 10


# Paddle class
class Paddle:
    def __init__(self, pos=(200, 400), size=(100, 20)):
        self.pos = list(pos)
        self.size = list(size)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.pos[0] = mouse_pos[0]

    def draw(self):
        screen.draw.filled_rect(Rect(self.pos+self.size), 'red')


# Ball class
class Ball:
    def __init__(self, pos=(200,300), vel=(2, -2)):
        self.pos = list(pos)
        self.vel = list(vel)
        self.radius = 10

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        for obstacle in obstacles:
            if touch(self, obstacle):
                obstacles.remove(obstacle)
                self.vel[1] = -self.vel[1]
        self.collide()

        # # check for collisions with the walls
        # if self.pos[0] > WIDTH - 20 or self.pos[0] < 20:
        #     self.vel[0] *= -1
        # if self.pos[1] < 20:
        #     self.vel[1] *= -1

        # # bounce off the paddle
        # if pygame.Rect.colliderect(paddle):
        #     self.vel[1] *= -1

    def collide(self):
        # Bounce off the sides of the screen
        if self.pos[0] + self.radius >= WIDTH or self.pos[0] - self.radius <= 0:
            self.vel[0] *= -1
        # Bounce off the paddle
        if (
            self.pos[1] + self.radius >= HEIGHT - 20
            and self.pos[0] + self.radius >= paddle.pos[0]
            and self.pos[0] - self.radius <= paddle.pos[0] + paddle.size[0]
        ):
            self.vel[1] *= -1
        # Reset position if the ball goes off the bottom
        if self.pos[1] - self.radius <= 0:
            self.pos[0] = WIDTH//2
            self.pos[1] = HEIGHT//2
            global lives
            lives -= 1

        # # bounce off the paddle
        # if self.colliderect(paddle):
        #     self.vel[1] *= -1
        #
        # # reset ball and lose a life, if falls below paddle
        # if self.pos[1] > paddle.pos[1] + 20:
        #     global lives
        #     lives -= 1
        #     self.x = WIDTH / 2
        #     self.y = HEIGHT - 60

    def draw(self):
        screen.draw.filled_circle(self.pos, self.radius, 'black')


# Obstacle class
class Obstacle:
    def __init__(self, pos=(30, 100), radius=20):
        self.pos = list(pos)
        self.radius = radius

    def draw(self):
        screen.draw.filled_circle(self.pos, self.radius, 'blue')


# Touch function to check for collision between ball and obstacles
def touch(ball, obstacle):
    dx = ball.pos[0]-obstacle.pos[0]
    dy = ball.pos[1]-obstacle.pos[1]
    distance = (dx*dx + dy*dy)**0.5
    return distance <= ball.radius + obstacle.radius

# Global Variables
ball = Ball()
paddle = Paddle()

# Generate Obstacles
for i in range(num_obstacles):
    x_pos = WIDTH/2 - 50 + i*50
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
        game_over = True

pgzrun.go()
