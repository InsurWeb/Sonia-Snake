import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

head_img = pygame.image.load("head.jpeg")
head_img = pygame.transform.scale(head_img, (CELL_SIZE, CELL_SIZE))

apple_img = pygame.image.load("apple.png")
apple_img = pygame.transform.scale(apple_img, (CELL_SIZE, CELL_SIZE))

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.color = (0, 255, 0)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * CELL_SIZE)) % WIDTH), (cur[1] + (y * CELL_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.score = 0

    def draw(self, surface):
        for p in self.positions[1:]:
            pygame.draw.rect(surface, self.color, (p[0], p[1], CELL_SIZE, CELL_SIZE))
        surface.blit(head_img, self.positions[0])


class Fruit:
    def __init__(self):
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                         random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        self.snake_head_position = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                                    random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

    def draw(self, surface):
        surface.blit(apple_img, self.position)


def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game // By Insur")

    snake = Snake()
    fruit = Fruit()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.turn((1, 0))

        snake.move()
        if snake.get_head_position() == fruit.position:
            snake.length += 1
            snake.score += 1
            fruit.randomize_position()

        window.fill(BLACK)
        snake.draw(window)
        fruit.draw(window)
        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()
