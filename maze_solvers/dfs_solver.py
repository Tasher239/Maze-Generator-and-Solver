from utils.maze import Maze
from utils.cell import Cell
from maze_solvers.base_solver import BaseSolver
from maze_generators.prim_generator import PrimGenerator


class DfsSolver(BaseSolver):
    """Класс поиска пути методом обхода в глубину (DFS)"""

    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.solver_name = "DFS"
        self.cur_dfs_path: list[Cell] = []
        self.visited: set[Cell] = set()
        self.best_path: list[Cell] = []
        self.best_cost: float = float("-inf")

    def find_path(self) -> None:
        """Находит путь от начальной точки до конечной методом обхода в глубину"""
        cur_point = self.maze.start_point
        self._dfs(cur_point)
        self.maze.paths_dict[self.solver_name] = self.best_path

    def _dfs(self, cur_point: Cell):
        self.cur_dfs_path.append(cur_point)
        self.visited.add(cur_point)

        if cur_point == self.maze.finish_point:
            self._update_best_path()
            self.cur_dfs_path.pop()
            self.visited.remove(cur_point)
            return

        for neighbour in self.maze.get_neighbors(cur_point):
            if neighbour not in self.visited:
                self._dfs(neighbour)

        self.visited.remove(cur_point)
        self.cur_dfs_path.pop()
        return None

    def _update_best_path(self) -> None:
        path_cost = self._calculate_path_cost()
        if path_cost > self.best_cost:
            self.best_cost = path_cost
            self.best_path = self.cur_dfs_path.copy()
        return None

    def _calculate_path_cost(self) -> int:
        total_cost = sum(cell.weight for cell in self.cur_dfs_path)
        return total_cost
