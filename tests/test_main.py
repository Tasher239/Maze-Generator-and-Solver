import unittest
from tests.test_invalid_inputs import (
    TestInvalidInputs,
    TestGetPointInMaze,
    TestGetMazeDimensions,
)
from tests.test_solvers import TestPathfindingAlgorithms
from tests.test_maze_display import TestMazeDisplay


def main():
    # Создаем загрузчик тестов
    loader = unittest.TestLoader()

    # Собираем тесты из всех классов
    test_suite = unittest.TestSuite()
    test_suite.addTests(loader.loadTestsFromTestCase(TestInvalidInputs))
    test_suite.addTests(loader.loadTestsFromTestCase(TestGetPointInMaze))
    test_suite.addTests(loader.loadTestsFromTestCase(TestGetMazeDimensions))
    test_suite.addTests(loader.loadTestsFromTestCase(TestPathfindingAlgorithms))
    test_suite.addTests(loader.loadTestsFromTestCase(TestMazeDisplay))

    # Запускаем тесты
    runner = unittest.TextTestRunner()
    runner.run(test_suite)


if __name__ == "__main__":
    main()
