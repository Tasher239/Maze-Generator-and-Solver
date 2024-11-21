import random
from utils.maze import Maze
from utils.cell import Cell
from maze_generators.base_generator import BaseGenerator


class PrimGenerator(BaseGenerator):
    """Генератор лабиринта алгоритмом Прима"""

    def __init__(
        self,
        width: int,
        height: int,
        good_surface: bool,
        bad_surface: bool,
        start_point: Cell,
        finish_point: Cell,
    ):
        super().__init__(
            width,
            height,
            good_surface,
            bad_surface,
            start_point,
            finish_point,
        )

    def generate(self) -> Maze:
        """Генерирует лабиринт с помощью алгоритма Прима"""
        start_cell = self.maze.table[0][0]
        edges_lst: list[tuple] = []  # список стен для добавления в очередь
        visited = set()
        visited.add((start_cell.i, start_cell.j))

        # Инициализируем начальные стены
        self._add_walls(start_cell, edges_lst)

        while edges_lst:
            # Выбираем случайную стену из очереди
            edge = random.choice(edges_lst)
            cell1, cell2 = edge

            if (cell2.i, cell2.j) not in visited or random.random() < 0.1:
                # Удаляем стену между cell1 и cell2
                self.maze.remove_wall(cell1, cell2)
                visited.add((cell2.i, cell2.j))
                self._add_walls(cell2, edges_lst)
            edges_lst.remove(edge)

        return self.maze

    def _add_walls(self, cell: Cell, edges_lst: list) -> None:
        """Добавляет стены соседних ячеек в список"""
        moves = [Cell(-1, 0, 0), Cell(1, 0, 0), Cell(0, 1, 0), Cell(0, -1, 0)]

        for delta_cell in moves:
            new_cell = delta_cell + cell
            if 0 <= new_cell.i < self.maze.height and 0 <= new_cell.j < self.maze.width:
                neighbor = self.maze.table[new_cell.i][new_cell.j]
                if (neighbor.i, neighbor.j) not in {
                    (c[0].i, c[0].j) for c in edges_lst
                }:
                    edges_lst.append((cell, neighbor))
        return None
