import random
from utils.cell import Cell
from abc import ABC


class Maze(ABC):
    """Класс для представления лабиринта"""

    def __init__(
        self,
        width: int,
        height: int,
        contain_positive_weight: bool,
        contain_negative_weight: bool,
        start_point: Cell,
        finish_point: Cell,
    ):
        self.width = width
        self.height = height
        self.contain_cell_with_weight = (
            contain_positive_weight or contain_negative_weight
        )
        self.table = self.make_table(contain_positive_weight, contain_negative_weight)

        self.start_point = start_point
        self.finish_point = finish_point
        self.paths_dict: dict[str, list[Cell]] = (
            {}
        )  # словарь для хранения путей (=последовательность клеток), полученных разными алгоритмами

    def make_table(
        self, contain_positive_weight: bool, contain_negative_weight: bool
    ) -> list[list[Cell]]:
        """Создаёт таблицу клеток с весами согласно заданным условиям"""
        if contain_positive_weight and contain_negative_weight:
            table = [
                [
                    (
                        self.create_cell_positive_weight(i, j)
                        if random.random() < 0.5
                        else self.create_cell_negative_weight(i, j)
                    )
                    for j in range(self.width)
                ]
                for i in range(self.height)
            ]
        elif contain_positive_weight:
            table = [
                [self.create_cell_positive_weight(i, j) for j in range(self.width)]
                for i in range(self.height)
            ]
        elif contain_negative_weight:
            table = [
                [self.create_cell_negative_weight(i, j) for j in range(self.width)]
                for i in range(self.height)
            ]
        else:
            table = [
                [Cell(i, j, 0) for j in range(self.width)] for i in range(self.height)
            ]

        return table

    @staticmethod
    def create_cell_positive_weight(i: int, j: int) -> Cell:
        """Создаёт ячейку с положительным весом"""
        if random.random() < 0.5:  # 50% вероятность
            weight = 0  # Нет штрафа
        else:
            weight = random.randint(1, 5)  # Вес от 1 по 5
        return Cell(i, j, weight)

    @staticmethod
    def create_cell_negative_weight(i: int, j: int) -> Cell:
        """Создаёт ячейку с отрицательным весом"""
        if random.random() < 0.5:  # 50% вероятность
            weight = 0  # Нет штрафа
        else:
            weight = random.randint(-5, -1)  # Вес от -5 по -1
        return Cell(i, j, weight)

    def get_around_cells(self, cell: Cell) -> list[Cell]:
        """Возвращает клетки вокруг заданной клетки"""
        around_cells = []
        moves = [Cell(-1, 0, 0), Cell(1, 0, 0), Cell(0, 1, 0), Cell(0, -1, 0)]

        for delta_cell in moves:
            new_cell = cell + delta_cell
            if self.is_valid_point(new_cell.i, new_cell.j):
                around_cells.append(self.table[new_cell.i][new_cell.j])
        return around_cells

    def get_neighbors(self, cell: Cell) -> list[Cell]:
        """Возвращает соседей клетки (нет стены между ними)"""
        neighbors = []
        moves = {
            "Up": Cell(-1, 0, 0),
            "Down": Cell(1, 0, 0),
            "Right": Cell(0, 1, 0),
            "Left": Cell(0, -1, 0),
        }

        for wall_direction, delta_cell in moves.items():
            new_cell = cell + delta_cell
            if (
                self.is_valid_point(new_cell.i, new_cell.j)
                and not cell.walls[wall_direction]
            ):
                neighbors.append(self.table[new_cell.i][new_cell.j])
        return neighbors

    @staticmethod
    def remove_wall(cell1: Cell, cell2: Cell) -> None:
        """Удаляет стену между двумя ячейками в заданном направлении"""
        delta_cell = cell1 - cell2
        if delta_cell.i == 1:
            wall_direction = "Up"
        elif delta_cell.i == -1:
            wall_direction = "Down"
        elif delta_cell.j == 1:
            wall_direction = "Left"
        else:
            wall_direction = "Right"

        cell1.walls[wall_direction] = False
        opposite_direction = {
            "Up": "Down",
            "Down": "Up",
            "Right": "Left",
            "Left": "Right",
        }
        cell2.walls[opposite_direction[wall_direction]] = False
        return None

    def is_valid_point(self, i: int, j: int) -> bool:
        """Проверяет, что координаты (i, j) находятся в пределах лабиринта"""
        return 0 <= i < self.height and 0 <= j < self.width

    def get_renderer_path(self, algorithm_name: str = "") -> str:
        """Визуализирует лабиринт с указанием направления пути из paths_dict"""
        res = ""
        path = self.paths_dict.get(algorithm_name, [])

        parent = {path[i]: path[i - 1] for i in range(1, len(path))}

        horizontal_wall = "═══"
        vertical_wall = "║"
        cross = "╬"
        left_right_down = "╦"
        left_right_up = "╩"
        left_up_corner = "╔"
        right_up_corner = "╗"
        left_down_corner = "╚"
        right_down_corner = "╝"
        up_down_left = "╣"
        up_down_right = "╠"
        mini_wall = "═"

        # directions = {(-1, 0): "↑", (1, 0): "↓", (0, -1): "←", (0, 1): "→"}
        directions = {
            (-1, 0): " \033[42;30m↑\033[0m ",
            (1, 0): " \033[42;30m↓\033[0m ",
            (0, -1): " \033[42;30m←\033[0m ",
            (0, 1): " \033[42;30m→\033[0m ",
        }

        for i in range(self.height):
            first_part = ""
            second_part = ""
            for j in range(self.width):
                cell = self.table[i][j]

                if i == 0 and j == 0:
                    first_part += left_up_corner + horizontal_wall
                elif i == 0 and not cell.walls["Left"]:
                    first_part += mini_wall + horizontal_wall
                elif i == 0:
                    first_part += left_right_down + horizontal_wall

                elif cell.walls["Up"]:
                    if (
                        not self.table[i - 1][j].walls["Left"]
                        and not cell.walls["Left"]
                    ):
                        first_part += mini_wall + horizontal_wall

                    elif j > 0 and not self.table[i - 1][j - 1].walls["Down"]:
                        if (
                            self.table[i - 1][j].walls["Left"]
                            and not cell.walls["Left"]
                        ):
                            first_part += left_down_corner + horizontal_wall
                        elif (
                            not self.table[i - 1][j].walls["Left"]
                            and cell.walls["Left"]
                        ):
                            first_part += left_up_corner + horizontal_wall
                        else:
                            first_part += up_down_right + horizontal_wall

                    elif self.table[i - 1][j].walls["Left"] and not cell.walls["Left"]:
                        first_part += left_right_up + horizontal_wall

                    elif not self.table[i - 1][j].walls["Left"] and cell.walls["Left"]:
                        first_part += left_right_down + horizontal_wall

                    elif (
                        self.table[i - 1][j].walls["Left"]
                        and cell.walls["Left"]
                        and (j == 0 or not self.table[i][j - 1].walls["Up"])
                    ):
                        first_part += up_down_right + horizontal_wall
                    else:
                        first_part += cross + horizontal_wall
                else:
                    if first_part.endswith(horizontal_wall):
                        if (
                            not self.table[i - 1][j].walls["Left"]
                            and not cell.walls["Left"]
                        ):
                            first_part += mini_wall + "   "
                        elif (
                            self.table[i - 1][j].walls["Left"]
                            and not cell.walls["Left"]
                        ):
                            first_part += right_down_corner + "   "
                        elif (
                            not self.table[i - 1][j].walls["Left"]
                            and cell.walls["Left"]
                        ):
                            first_part += right_up_corner + "   "
                        else:
                            first_part += up_down_left + "   "
                    else:
                        first_part += vertical_wall + "   "

                arrow = " "
                if cell == self.start_point:
                    arrow = "A"
                elif cell == self.finish_point:
                    arrow = "B"
                elif cell in path:
                    previous_cell = parent.get(cell, None)
                    delta_cell = cell - previous_cell
                    delta_i, delta_j = delta_cell.i, delta_cell.j
                    arrow = directions.get((delta_i, delta_j), "")
                elif self.contain_cell_with_weight:
                    arrow = str(cell.weight) if cell.weight != 0 else " "

                second_part += (
                    vertical_wall if cell.walls["Left"] else " "
                ) + f"{arrow:^3}"

            if i == 0:
                first_part += right_up_corner
            else:
                if first_part.endswith(horizontal_wall):
                    first_part += up_down_left
                else:
                    first_part += vertical_wall
            if second_part.endswith(horizontal_wall):
                second_part += up_down_left
            else:
                second_part += vertical_wall

            res += first_part + "\n" + second_part + "\n"

        last_row = left_down_corner + horizontal_wall
        for j in range(1, self.width):
            cell = self.table[self.height - 1][j]
            if cell.walls["Left"]:
                last_row += left_right_up + horizontal_wall
            else:
                last_row += mini_wall + horizontal_wall
        last_row += right_down_corner
        res += last_row + "\n"

        return res
