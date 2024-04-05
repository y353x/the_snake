from random import randint
import pygame as pg

# Инициализация PyGame:
pg.init()

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Родительский класс для классов змейки и яблока"""

    def __init__(self, body_color=None):
        self.body_color = body_color
        # Начальная позиция.
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        """Метод для отрисовки объекта на игровом поле,
        содержимое которого определяется в дочерних классах.
        """


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    # При использовании {snake_positions=None} - не проходит Pytest.
    # Параметр (0, 0) только ради прохождения проверки платформы.
    def __init__(self, snake_positions=(0, 0), body_color=APPLE_COLOR):
        # Вызов функции рандом позиции.
        super().__init__(body_color=body_color)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Функция формирования случайной позиции яблока
        (в зависимости от положения змейки)
        """
        while True:
            # Присваиваем случайные координаты Х и У.
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            # Если self.position не в теле змейки.
            if self.position not in snake_positions:
                break
            else:
                continue

    # Метод draw класса Apple из прекода.
    def draw(self):
        """Функция отрисовки яблоки с нужным цветом и позицией"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        # Начальные параметры length, positions,
        # direction, next_direction, согласно ТЗ.
        self.reset()

    def update_direction(self, next_direction=None):
        """Обновляет направление движения змейки."""
        if next_direction:
            self.direction = next_direction

    def move(self, object_apple):
        """Обновляет позицию змейки, добавляя новую голову и удаляя
        последний элемент, если длина змейки не увеличилась.
        """
        # Распаковка позиции головы змейки, направления движения.
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        # Остаток от деления для случаев выхода за границы поля.
        new_position_x = (head_x
                          + direction_x * GRID_SIZE) % SCREEN_WIDTH
        new_position_y = (head_y
                          + direction_y * GRID_SIZE) % SCREEN_HEIGHT

        # Добавление нового элемента (головы) в начало змейки.
        new_position = (new_position_x, new_position_y)
        self.positions.insert(0, new_position)

        if self.check_apple(object_apple):  # Чек столкновения с яблоком.
            self.length += 1  # При столкновении - увеличение длины.
            # Новое положение яблока.
            object_apple.randomize_position(self.positions)

        # Удаление последнего элемента змейки, если не съедено яблоко.
        if len(self.positions) == self.length:
            self.last = False
        else:
            self.last = self.positions[-1]
            self.positions.pop()

    def draw(self, renew=False):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки.
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        # Очистка следов змейки при столкновении с собой.
        if renew:
            screen.fill(BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        self.length = 1
        self.positions = [self.position]
        self.last = False
        self.direction = RIGHT  # Исходное направление движения.
        self.next_direction = None

    def check_apple(self, object_apple):
        """Проверка, съела ли змейка яблоко."""
        if self.get_head_position() == object_apple.position:
            return True
        else:
            return False


def handle_keys(game_object):
    """Обработка событий клавиш"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
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
        # Обновление направления движения.
        green_snake.update_direction(green_snake.next_direction)
        green_snake.move(red_apple)  # Движение змеи.
        if green_snake.get_head_position() in green_snake.positions[1:]:
            green_snake.reset()
            green_snake.draw(True)  # Отрисовка со сбросом.
        else:
            green_snake.draw()  # Отрисовка змейки.
        pg.display.update()  # Обновление экрана.


if __name__ == '__main__':
    main()
