from utils.maze import Maze
from typing import Any
from abc import ABC, abstractmethod


class BaseSolver(ABC):
    """Базовый класс для всех алгоритмов поиска пути"""

    def __init__(self, maze: Maze):
        self.solver_name: str = ""
        self.maze = maze
        self.parent: dict[Any, Any] = {}
        self.solver_name: str

    @abstractmethod
    def find_path(self) -> None:
        """Метод для решения лабиринта. Должен быть переопределён в подклассах"""
        pass
