from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 3

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """написать docstring"""

    position = (16 * GRID_SIZE, 12 * GRID_SIZE)  # Начальная позиция (центр) ?

    def __init__(self, body_color):
        self.position = GameObject.position
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    """написать docstring"""

    body_color = (255, 0, 0)  # Задается красный цвет, статичный.

    def __init__(self):
        self.body_color = Apple.body_color
        # Вызов функции рандом позиции.
        self.position = Apple.randomize_position()

    @staticmethod
    def randomize_position():
        position_x = randint(0, 32) * GRID_SIZE
        position_y = randint(0, 24) * GRID_SIZE
        # Или return (randint(0,32), randint(0,24)).
        return (position_x, position_y)

    # Метод draw класса Apple из прекода.
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """написать docstring"""

    # length = 1
    body_color = (0, 255, 0)
    # position = ...
    # positions: list = [GameObject.position]
    direction = RIGHT
    # next_direction = None

    def __init__(self):  # Инициализирует начальное состояние змейки.
        self.length = 1
        self.next_direction = None
        self.positions = [GameObject.position]
        # self.last = self.positions[:-1]

    # Метод обновления направления после нажатия на кнопку
    # Из прекода.
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # обновляет позицию змейки (координаты каждой секции), добавляя новую
    # голову в начало списка positions и удаляя последний элемент, если длина
    # змейки не увеличилась.
    def move(self):
        if self.direction == UP:
            new_position = (self.positions[0][0] + UP[0] * GRID_SIZE,
                            self.positions[0][1] + UP[1] * GRID_SIZE)
            self.positions.insert(0, new_position)
        elif self.direction == DOWN:
            new_position = (self.positions[0][0] + DOWN[0] * GRID_SIZE,
                            self.positions[0][1] + DOWN[1] * GRID_SIZE)
            self.positions.insert(0, new_position)
        elif self.direction == RIGHT:
            new_position = (self.positions[0][0] + RIGHT[0] * GRID_SIZE,
                            self.positions[0][1] + RIGHT[1] * GRID_SIZE)
            self.positions.insert(0, new_position)
        elif self.direction == LEFT:
            new_position = (self.positions[0][0] + LEFT[0] * GRID_SIZE,
                            self.positions[0][1] + LEFT[1] * GRID_SIZE)
            self.positions.insert(0, new_position)
        self.last = self.positions[-1]
        self.positions.pop()

    # Метод draw класса Snake из прекода
    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    # возвращает позицию головы змейки (первый элемент в списке positions).
    def get_head_position(self):
        return self.positions[0]

    def reset():  # сброс змеи после столкновения с собой.
        pass


# Функция обработки действий пользователя
def handle_keys(game_object):
    """написать docstring"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """написать docstring"""
    # Тут нужно создать экземпляры классов.
    red_apple = Apple()
    green_snake = Snake()
    screen

    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        red_apple.randomize_position()
        red_apple.draw()
        handle_keys(green_snake)
        green_snake.update_direction()
        green_snake.move()
        green_snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None



    # def move(self):
    #     if self.next_direction == UP:
    #         new_position = (self.positions[0][0] + UP[0] * GRID_SIZE,
    #                         self.positions[0][1] + UP[1] * GRID_SIZE)
    #         print(new_position)
    #         self.positions.insert(0, new_position)
    #     elif self.next_direction == DOWN:
    #         new_position = (self.positions[0][0] + DOWN[0] * GRID_SIZE,
    #                         self.positions[0][1] + DOWN[1] * GRID_SIZE)
    #         self.positions.insert(0, new_position)
    #     elif self.next_direction == RIGHT:
    #         new_position = (self.positions[0][0] + RIGHT[0] * GRID_SIZE,
    #                         self.positions[0][1] + RIGHT[1] * GRID_SIZE)
    #         self.positions.insert(0, new_position)
    #     elif self.next_direction == LEFT:
    #         new_position = (self.positions[0][0] + LEFT[0] * GRID_SIZE,
    #                         self.positions[0][1] + LEFT[1] * GRID_SIZE)
    #         self.positions.insert(0, new_position)

    #     self.last = self.positions[-1]