from random import choice, randint


# Тут опишите все классы игры.
class GameObject:
    # position = (16, 12) # Начальная позиция (центр) ? 

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    body_color = (255, 0, 0)

    def __init__(self):
        self.body_color = Apple.body_color
        self.position = Apple.randomize_position()

    def randomize_position():
        position_x = randint(0,32)
        position_y = randint(0,24)
        return (position_x, position_y)
    

object = Apple()
print(object.position)
print(object.body_color)
