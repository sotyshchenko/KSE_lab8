import pgzrun
import pygame
import random
from pgzero.actor import Actor
from vector import Vector

# # Position ball at the center of the screen.
# ball.pos = (WIDTH/2, HEIGHT/2)
# # Position paddle at the bottom of the screen.
# paddle.pos = (WIDTH/2, HEIGHT - paddle.height)
# # Position obstacle randomly on the top of the screen.
# obstacle.pos = (random.randint(0,WIDTH), 0)
WIDTH = 500
HEIGHT = 500
HEART_RADIUS = 20
lives = 3
heart = Actor('heart')
heart.pos = [5, 20]
bonus_life = Actor('bonus_life')
#bonus_paddle =


# Paddle class
class Paddle:
    def __init__(self, pos=(200, 400), size=(100, 20)):
        self.pos = list(pos)
        self.size = list(size)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.pos[0] = mouse_pos[0]

    def draw(self):
        screen.draw.filled_rect(Rect(self.pos + self.size), "black")


# Ball class
class Ball:
    def __init__(self, pos=(200, 300), vel=(3, -3)):
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
        self.touch_element()

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

    def touch_element(self):
        for obstacle in obstacles:
            if obstacle.y - obstacle.radius <= self.pos[1] - self.radius <= obstacle.y + obstacle.radius and \
                    obstacle.x - obstacle.radius <= self.pos[0] - self.radius <= obstacle.x + obstacle.radius:
                self.vel[1] *= -1
                obstacle.damage -= 1
            elif obstacle.y - obstacle.radius + 6 >= self.pos[1] + self.radius and \
                    obstacle.x - obstacle.radius - 3 <= self.pos[0] - self.radius <= obstacle.x + obstacle.radius + 3:
                self.vel[1] *= 1
                obstacle.damage -= 1
            if obstacle.damage == 0:
                obstacles.remove(obstacle)
                self.increase_velocity()

    def increase_velocity(self):
        #increases velocity of the ball with each obstacle removed.
        if len(obstacles) >= 0:
            self.vel[0] = self.vel[0] * 1.05
            self.vel[1] = self.vel[1] * 1.05
            if self.vel[0] > 4:
                self.vel[0] = 4
            if self.vel[1] > 4:
                self.vel[1] = 4

    def draw(self):
        screen.draw.filled_circle(self.pos, self.radius, "red")


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


# Class Bonus Life
class Bonus_life:
    def __init__(self, pos: Vector):
        self.actor = Actor('bonus_life')
        self.pos = pos
        self.x = x
        self.y = y
        self.velocity = Vector(0, 100)

    def move(self, dt):
        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), 5, "red")
        #self.actor.draw(self.x, self.y)

    def hits(self, paddle:Paddle):
        paddle.pos = paddle.pos[0], paddle.pos[1]
        distance = (paddle.pos() - self.pos).magnitude()
        return distance < 20
    #def collides_with(self, paddle):
        #if (
            #self.x - self.width//2 < paddle.pos[0] < self.x + self.width//2
            #and self.y - self.height // 2 < paddle.pos[1] < self.y + self.height // 2
        #):
            #return True
        #return False

#class Bonus_paddle:


# # Touch function to check for collision between ball and obstacles
# def touch(ball, obstacle):
#     dx = ball.pos[0] - obstacle.x
#     dy = ball.pos[1] - obstacle.y
#     distance = (dx * dx + dy * dy) ** 0.5
#     return distance <= ball.radius + obstacle.radius

# Global Variables
ball = Ball()
paddle = Paddle()
obstacles = []  # obstacles list
rows = 3  # obstacle rows
bonuses = []

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
    for bonus in bonuses:
        bonus.draw()
    for obstacle in obstacles:
        obstacle.draw()

    for i in range(lives):
        #x_pos =  heart.pos[0] + 10
        x_pos = 20 + i * HEART_RADIUS * 2
        heart.pos = x_pos, heart.pos[1]
        heart.draw()
        #x_pos = 20 + i * HEART_RADIUS * 2
        #screen.draw.filled_circle((x_pos, HEART_RADIUS), HEART_RADIUS, "pink")
    # Check if the game is over.
    if lives < 1:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=60)

    elif len(obstacles) == 0:
        screen.draw.text("YOU WON", center=(WIDTH // 2, HEIGHT // 2), fontsize=60)



def update(dt):
    ball.update()
    paddle.update()
    if random.random() < 0.01:
        bonuses.append(Bonus_life(Vector(random.randint(0, WIDTH), -10)))
    for bonus in bonuses:
        bonus.move(dt)
        if bonus.hits(paddle):
            global lives
            lives = lives + 1
            bonuses.remove(bonus)
    # for obstacle in obstacles:
    #     if (
    #         obstacle.x - obstacle.radius < ball.pos[0] < obstacle.x + obstacle.radius and
    #         obstacle.y - obstacle.radius < ball.pos[1] < obstacle.y + obstacle.radius
    #     ):
    #         obstacle.damage -= 1
    #         if abs(ball.pos[0] - (obstacle.x - obstacle.radius)) < abs(ball.pos[0] - (obstacle.x + obstacle.radius)):
    #             ball.vel[0] = -ball.vel[0]
    #         else:
    #             ball.vel[1] = -ball.vel[1]
    #         if obstacle.damage == 0:
    #             obstacles.remove(obstacle)


def on_mouse_move(pos):
    paddle.update()

pgzrun.go()
