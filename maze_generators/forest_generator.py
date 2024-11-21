from maze_generators.base_generator import BaseGenerator
from maze_generators.kruskal_generator import SNM
import random
from utils.maze import Maze
from utils.cell import Cell


class GrowingForestGenerator(BaseGenerator):
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
            width, height, good_surface, bad_surface, start_point, finish_point
        )
        self.snm = SNM(width, height)

    def generate(self) -> Maze:
        # Список всех возможных ребер (соседних клеток)
        edges = []
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                if i < self.maze.height - 1:  # Стена вниз
                    edges.append(((i, j), (i + 1, j)))
                if j < self.maze.width - 1:  # Стена вправо
                    edges.append(((i, j), (i, j + 1)))
        random.shuffle(edges)

        for cell1, cell2 in edges:
            if self.snm.find_parent(cell1) != self.snm.find_parent(cell2):
                # Удаляем стену между cell1 и cell2
                self.maze.remove_wall(
                    self.maze.table[cell1[0]][cell1[1]],
                    self.maze.table[cell2[0]][cell2[1]],
                )

                self.snm.union(cell1, cell2)

        return self.maze
