from utils.maze import Maze
from utils.cell import Cell
from maze_solvers.base_solver import BaseSolver


class FordBellmanSolver(BaseSolver):
    """Класс поиска пути методом Форда-Беллмана с учётом весов клеток"""

    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.solver_name = "Ford-Bellman"
        self.dist: dict[Cell, float] = {}

    def initialize(self, start: Cell):
        # Инициализируем расстояния и родительские клетки
        for row in self.maze.table:
            for cell in row:
                self.dist[cell] = float("-inf")
                self.parent[cell] = None
        self.dist[start] = 0  # Расстояние до начальной клетки равно 0

    def find_path(self) -> None:
        """Находит путь максимальной стоимости от start до end с помощью алгоритма Форда-Беллмана"""
        self.initialize(self.maze.start_point)

        # Основной цикл Форда-Беллмана
        for _ in range(len(self.maze.table) * len(self.maze.table[0]) - 1):
            for row in self.maze.table:
                for cell in row:
                    for neighbor in self.maze.get_neighbors(cell):
                        # Обновляем расстояние с учётом веса (штрафа) клетки
                        if self.dist[cell] + neighbor.weight > self.dist[neighbor]:
                            self.dist[neighbor] = self.dist[cell] + neighbor.weight
                            self.parent[neighbor] = cell

        # Восстанавливаем путь
        path = []
        current_cell = self.maze.finish_point
        while current_cell is not None:
            path.append(current_cell)
            current_cell = self.parent[current_cell]

        path.reverse()  # Переворачиваем путь, чтобы он был от start до end
        self.maze.paths_dict[self.solver_name] = path
        return None
