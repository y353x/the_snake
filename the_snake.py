from random import randint

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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс для классов змейки и яблока"""

    position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Начальная позиция.

    def __init__(self, body_color=None):
        self.body_color = body_color

    def draw(self):
        """Заготовка метода для отрисовки объекта на игровом поле."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    body_color = (255, 0, 0)  # Задается красный цвет, статичный.

    def __init__(self):
        # Вызов функции рандом позиции.
        self.position = Apple.randomize_position()

    @staticmethod
    def randomize_position():
        """Функция формирования случайной позиции яблока"""
        position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (position_x, position_y)

    # Метод draw класса Apple из прекода.
    def draw(self):
        """Функция отрисовки яблоки с нужным цветом и позицией"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    length = 1  # Исходная длина змейки.
    body_color = (0, 255, 0)  # Задается зелёный цвет, статичный.
    direction = RIGHT  # Исходное направление движения змейки.
    next_direction = None  # заготовка под новое направление движения.

    def __init__(self):  # Инициализирует начальное состояние змейки.
        self.positions = [GameObject.position]  # Список элементов тела змейки.

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, object_apple):
        """Обновляет позицию змейки, добавляя новую голову и удаляя
        последний элемент, если длина змейки не увеличилась.
        """
        new_position_x = (self.positions[0][0] + self.direction[0] * GRID_SIZE)
        new_position_y = (self.positions[0][1] + self.direction[1] * GRID_SIZE)
        # Далее описание случаев выхода за границы поля.
        if new_position_x >= SCREEN_WIDTH:
            new_position_x -= SCREEN_WIDTH
        elif new_position_x < 0:
            new_position_x += SCREEN_WIDTH

        if new_position_y >= SCREEN_HEIGHT:
            new_position_y -= SCREEN_HEIGHT
        elif new_position_y < 0:
            new_position_y += SCREEN_HEIGHT

        # Добавление нового элемента (головы) в начало змейки.
        new_position = (new_position_x, new_position_y)
        self.positions.insert(0, new_position)

        if self.check_apple(object_apple):  # Чек столкновения с яблоком.
            self.length += 1  # При столкновении - увеличение длины.

        # Удаление последнего элемента змейки, если не съедено яблоко.
        if len(self.positions) == self.length:
            self.last = None
        else:
            self.last = self.positions[-1]
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
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

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        for element in self.positions[1:]:
            if self.get_head_position() == element:
                for element in self.positions:
                    old_snake = pygame.Rect(element, (GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, old_snake)
                return True

    def check_apple(self, object_apple):
        """Проверка, съела ли змейка яблоко."""
        if self.get_head_position() == object_apple.position:
            return True
        else:
            return False


def handle_keys(game_object):
    """Обработка событий клавиш"""
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
    """Последовательность действий, описывающих логику работы игры"""
    # Исходные экземпляры классов.
    red_apple = Apple()  # Создание объекта "яблоко".
    green_snake = Snake()  # Создание объекта "змейка".
    while True:
        clock.tick(SPEED)
        red_apple.draw()  # Отрисовка яблока.
        handle_keys(green_snake)  # Нажатие кнопок на клавиатуре.
        green_snake.update_direction()  # Обновление направления движения.
        green_snake.move(red_apple)  # Движение змеи.
        if green_snake.check_apple(red_apple):  # Проверка на съедение яблока.
            red_apple = Apple()  # Создание нового объекта "яблоко".
        green_snake.draw()  # Отрисовка змейки.
        pygame.display.update()  # Обновление экрана.
        if green_snake.reset():  # Проверка на столкновение с собой.
            green_snake = Snake()  # Создание нового объекта "змейка".


if __name__ == '__main__':
    main()
