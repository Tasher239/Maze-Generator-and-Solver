class Cell:
    """Класс для представления ячейки лабиринта"""

    def __init__(self, i: int, j: int, weight: int):
        self.i = i  # индекс строки
        self.j = j  # индекс строки
        self.weight = weight  # штраф, который получает игрок, попадая в эту клетку
        self.walls = {"Up": True, "Down": True, "Right": True, "Left": True}

    def __sub__(self, other):
        return Cell(self.i - other.i, self.j - other.j, self.weight - other.weight)

    def __add__(self, other):
        return Cell(self.i + other.i, self.j + other.j, self.weight + other.weight)

    def __iadd__(self, other):
        self.i += other.i
        self.j += other.j
        return self

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __hash__(self):
        return hash((self.i, self.j))
