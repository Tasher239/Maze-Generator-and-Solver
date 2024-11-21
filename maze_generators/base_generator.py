from utils.maze import Maze
from utils.cell import Cell
from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    def __init__(
        self,
        width: int,
        height: int,
        good_surface: bool,
        bad_surface: bool,
        start_point: Cell,
        finish_point: Cell,
    ):
        self.maze = Maze(
            width, height, good_surface, bad_surface, start_point, finish_point
        )

    @abstractmethod
    def generate(self) -> Maze:
        """Метод для генерации лабиринта. Должен быть переопределён в подклассах"""
        pass
