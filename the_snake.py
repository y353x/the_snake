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
SPEED = 10

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
        position_x = randint(0, 31) * GRID_SIZE
        position_y = randint(0, 23) * GRID_SIZE
        # Или return (randint(0,32), randint(0,24)).
        return (position_x, position_y)

    # Метод draw класса Apple из прекода.
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """написать docstring"""

    length = 1
    body_color = (0, 255, 0)
    direction = RIGHT
    next_direction = None

    def __init__(self):  # Инициализирует начальное состояние змейки.
        self.positions = [GameObject.position]

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
        new_position_x = (self.positions[0][0] + self.direction[0] * GRID_SIZE)
        new_position_y = (self.positions[0][1] + self.direction[1] * GRID_SIZE)
        if new_position_x > SCREEN_WIDTH:
            new_position_x -= SCREEN_WIDTH
        elif new_position_x < 0:
            new_position_x += SCREEN_WIDTH

        if new_position_y > SCREEN_HEIGHT:
            new_position_y -= SCREEN_HEIGHT
        elif new_position_y < 0:
            new_position_y += SCREEN_HEIGHT
        new_position = (new_position_x, new_position_y)
        self.positions.insert(0, new_position)

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

    def reset(self):  # сброс змеи после столкновения с собой.
        for element in self.positions[1:]:
            if self.get_head_position() == element:
                for element in self.positions:
                    old_snake = pygame.Rect(element, (GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, old_snake)
                return True

    def check_apple(self, object_apple):
        if self.get_head_position() == object_apple.position:
            self.length += 1  # Над решить...
            self.last = None
            return True
        else:
            self.last = self.positions[-1]
            self.positions.pop()
            return False


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
    # Исходные экземпляры классов.
    red_apple = Apple()
    green_snake = Snake()
    while True:
        clock.tick(SPEED)
        red_apple.draw()  # Отрисовка яблока
        handle_keys(green_snake)  # Нажатие кнопок на клавиатуре
        green_snake.update_direction()  # Обновление направления движения
        green_snake.move()  # движение змеи
        if green_snake.check_apple(red_apple):  # Проверка на съедание яблока
            red_apple = Apple()  # Создание нового объекта "Яблоко"
        green_snake.draw()  # Отрисовка змеи
        pygame.display.update()  # обновление экрана
        if green_snake.reset():  # Проверка на столкновение с собой
            green_snake = Snake()  # Создание нового объекта "Змея"


if __name__ == '__main__':
    main()


# если будут ошибки, игнорить