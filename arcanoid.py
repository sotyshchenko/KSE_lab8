import pgzrun
import pygame
import random

# # Position ball at the center of the screen.
# ball.pos = (WIDTH/2, HEIGHT/2)
# # Position paddle at the bottom of the screen.
# paddle.pos = (WIDTH/2, HEIGHT - paddle.height)
# # Position obstacle randomly on the top of the screen.
# obstacle.pos = (random.randint(0,WIDTH), 0)
TITLE = "Christmas Arkanoid"
WIDTH = 500
HEIGHT = 500
HEART_RADIUS = 20
global lives
lives = 3
num_obstacles = 6


# Paddle class
class Paddle:
    def __init__(self, pos=(200, 400), size=(100, 20)):
        self.pos = list(pos)
        self.size = list(size)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.pos[0] = mouse_pos[0]

    def draw(self):
        screen.draw.filled_rect(Rect(self.pos + self.size), "red")


# Ball class
class Ball:
    def __init__(self, pos=(200, 300), vel=(2, -2)):
        self.pos = list(pos)
        self.vel = list(vel)
        self.radius = 10

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        # for obstacle in obstacles:
        #     if touch(self, obstacle):
        #         obstacles.remove(obstacle)
        #         self.vel[1] = -self.vel[1]
        self.collide()

    def collide(self):
        # Bounce off the sides of the screen
        if self.pos[0] + self.radius >= WIDTH or self.pos[0] - self.radius <= 0:
            self.vel[0] *= -1
        # Bounce off paddle
        if (
            self.pos[0] + self.radius >= paddle.pos[0]
            and self.pos[0] <= paddle.pos[0] + paddle.size[0]
            and self.pos[1] + self.radius >= paddle.pos[1]
        ):
            self.vel[1] = -self.vel[1]
        # Bounce off ceiling
        if self.pos[1] + self.radius >= HEIGHT or self.pos[1] - self.radius <= 0:
            # Reset position if the ball goes off the bottom
            if self.pos[1] + self.radius >= HEIGHT:
                global lives
                lives = lives - 1
                self.pos[1] = paddle.pos[1] - self.radius
                self.pos[0] = paddle.pos[0] + paddle.size[1] / 2
            self.vel[1] = -self.vel[1]

    def draw(self):
        screen.draw.filled_circle(self.pos, self.radius, "black")


# Obstacle class
class Obstacle:
    def __init__(self, x, y, damage, color, radius=15):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.color = color
        self.radius = radius
        self.damage = damage

    def collides_with(self, ball):
        if (
            self.x - self.width//2 < ball.pos[0] < self.x + self.width//2
            and self.y - self.height // 2 < ball.pos[1] < self.y + self.height // 2
        ):
            return True
        return False

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, self.color)


# Touch function to check for collision between ball and obstacles
def touch(ball, obstacle):
    dx = ball.pos[0] - obstacle.x
    dy = ball.pos[1] - obstacle.y
    distance = (dx * dx + dy * dy) ** 0.5
    return distance <= ball.radius + obstacle.radius


# Global Variables
ball = Ball()
paddle = Paddle()
obstacles = []  # obstacles list
rows = 3  # obstacle rows

# Generate Obstacles
for row in range(3):
    for col in range(10):
        x = col * 50 + 30
        y = row * 40 + 60
        damage = random.randint(1, 3)
        color = (173, 216, 230) if damage == 1 else (0, 0, 255) if damage == 2 else (0, 0, 139)
        obstacles.append(Obstacle(x, y, damage, color))


def draw():
    screen.fill((198,168,104))
    paddle.draw()
    ball.draw()

    for obstacle in obstacles:
        obstacle.draw()
    for i in range(lives):
        x_pos = 20 + i * HEART_RADIUS * 2
        screen.draw.filled_circle((x_pos, HEART_RADIUS), HEART_RADIUS, "pink")


def update():
    ball.update()
    paddle.update()
    for obstacle in obstacles:
        if (
            obstacle.x - obstacle.radius < ball.pos[0] < obstacle.x + obstacle.radius and
            obstacle.y - obstacle.radius < ball.pos[1] < obstacle.y + obstacle.radius
        ):
            obstacle.damage -= 1
            if abs(ball.pos[0] - (obstacle.x - obstacle.radius)) < abs(ball.pos[0] - (obstacle.x + obstacle.radius)):
                ball.vel[0] = -ball.vel[0]
            else:
                ball.vel[1] = -ball.vel[1]
            if obstacle.damage == 0:
                obstacles.remove(obstacle)
    # Check if the game is over.
    if lives < 1:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=60)
    elif len(obstacles) == 0:
        screen.draw.text("YOU WON", center=(WIDTH // 2, HEIGHT // 2), fontsize=60)


def on_mouse_move(pos):
    paddle.update()

pgzrun.go()
