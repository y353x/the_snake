from random import randint
import pygame as py  # Сокращение, согласно замечанию.

# Инициализация PyGame:
py.init()

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
SPEED = 20

# Настройка игрового окна:
screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
py.display.set_caption('Змейка')

# Настройка времени:
clock = py.time.Clock()


class GameObject:
    """Родительский класс для классов змейки и яблока"""

    def __init__(self, body_color=None):
        self.body_color = body_color
        # Начальная позиция.
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        """Заготовка метода для отрисовки объекта на игровом поле."""


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, snake_positions=(0,0)):
        # Вызов функции рандом позиции.
        super().__init__(body_color=APPLE_COLOR)
        self.snake_positions = snake_positions
        self.position = self.randomize_position()

    def randomize_position(self):
        """Функция формирования случайной позиции яблока
        (в зависимости от положения змейки)
        """
        while True:
            # Присваиваем рандом координаты Х и У.
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            # Если self.position не в теле змейки.
            if self.position not in self.snake_positions:
                return self.position
            else:
                continue

    # Метод draw класса Apple из прекода.
    def draw(self):
        """Функция отрисовки яблоки с нужным цветом и позицией"""
        rect = py.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        py.draw.rect(screen, self.body_color, rect)
        py.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    direction = RIGHT  # Исходное направление движения змейки.
    next_direction = None  # заготовка под новое направление движения.

    # Инициализирует начальное состояние змейки.
    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.positions = [self.position]
        self.length = 1
        self.last = False

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, object_apple):
        """Обновляет позицию змейки, добавляя новую голову и удаляя
        последний элемент, если длина змейки не увеличилась.
        """
        # Остаток от деления для случаев выхода за границы поля.
        new_position_x = (self.get_head_position()[0]
                          + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_position_y = (self.get_head_position()[1]
                          + self.direction[1] * GRID_SIZE) % SCREEN_WIDTH

        # Добавление нового элемента (головы) в начало змейки.
        new_position = (new_position_x, new_position_y)
        self.positions.insert(0, new_position)

        if self.check_apple(object_apple):  # Чек столкновения с яблоком.
            self.length += 1  # При столкновении - увеличение длины.

        # Удаление последнего элемента змейки, если не съедено яблоко.
        if len(self.positions) == self.length:
            self.last = False
        else:
            self.last = self.positions[-1]
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (py.Rect(position, (GRID_SIZE, GRID_SIZE)))
            py.draw.rect(screen, self.body_color, rect)
            py.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = py.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        py.draw.rect(screen, self.body_color, head_rect)
        py.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = py.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            py.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        # Удаляет оставшиеся части змейки с экрана, подготавливая к новой игре.
        if self.reset():
            screen.fill(BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        for element in self.positions[1:]:
            if self.get_head_position() == element:
                self.length = 1
                self.positions = [self.position]
                self.direction = RIGHT
                return True

    def check_apple(self, object_apple):
        """Проверка, съела ли змейка яблоко."""
        if self.get_head_position() == object_apple.position:
            return True
        else:
            return False


def handle_keys(game_object):
    """Обработка событий клавиш"""
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            raise SystemExit
        elif event.type == py.KEYDOWN:
            if event.key == py.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == py.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == py.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == py.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Последовательность действий, описывающих логику работы игры"""
    # Исходные экземпляры классов.
    green_snake = Snake()  # Создание объекта "змейка".
    red_apple = Apple(green_snake.positions)  # Создание объекта "яблоко".
    while True:
        clock.tick(SPEED)
        red_apple.draw()  # Отрисовка яблока.
        handle_keys(green_snake)  # Нажатие кнопок на клавиатуре.
        green_snake.update_direction()  # Обновление направления движения.
        green_snake.move(red_apple)  # Движение змеи.
        if green_snake.check_apple(red_apple):  # Проверка на съедение яблока.
            # Создание нового объекта "яблоко".
            red_apple = Apple(green_snake.positions)
        green_snake.draw()  # Отрисовка змейки.
        py.display.update()  # Обновление экрана.


if __name__ == '__main__':
    main()
