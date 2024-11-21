import random
from utils.maze import Maze
from utils.cell import Cell
from maze_generators.base_generator import BaseGenerator


class KruskalGenerator(BaseGenerator):
    """Генератор лабиринта алгоритмом Крускала"""

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
        self.snm_method = SNM(width, height)
        self.edges = self._create_edges()

    def _create_edges(self):
        """создаём список всех рёбер, вершины которых - 2 соседние по стороне клетки лабиринта"""
        edges = []
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                cell = self.maze.table[i][j]
                for neighbor in self.maze.get_around_cells(cell):
                    if (neighbor.i, neighbor.j) > (
                        cell.i,
                        cell.j,
                    ):  # не дублируем рёбра
                        edges.append((cell, neighbor))
        random.shuffle(edges)  # шафлим рёбра для случайного обхода
        return edges

    def generate(self):
        """Генерирует лабиринт, удаляя стены согласно алгоритму Крускала"""
        for cell1, cell2 in self.edges:
            root1 = self.snm_method.find_parent((cell1.i, cell1.j))
            root2 = self.snm_method.find_parent((cell2.i, cell2.j))
            if root1 != root2 or random.random() < 0.1:
                self.maze.remove_wall(cell1, cell2)
                self.snm_method.union((cell1.i, cell1.j), (cell2.i, cell2.j))
        return self.maze


class SNM:
    """Класc реализации сжатия путей"""

    def __init__(self, width, height):
        self.parent = {(i, j): (i, j) for i in range(height) for j in range(width)}
        self.set_size = {(i, j): 1 for i in range(height) for j in range(width)}

    def find_parent(self, cell):
        if self.parent[cell] != cell:
            self.parent[cell] = self.find_parent(self.parent[cell])
        return self.parent[cell]

    def union(self, cell1, cell2):
        root1 = self.find_parent(cell1)
        root2 = self.find_parent(cell2)
        if root1 != root2:
            # к меньшему дереву подвешиваем большее
            if self.set_size[root1] > self.set_size[root2]:
                root1, root2 = root2, root1
            self.parent[root1] = root2
            self.set_size[root2] += self.set_size[root1]
