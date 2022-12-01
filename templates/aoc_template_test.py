import importlib
import pytest

from pathlib import Path

problem_file = importlib.import_module(Path(__file__).stem[:-5])


@pytest.fixture
def sample_input():
    return problem_file.parse_input(problem_file.SAMPLE_PATH)


@pytest.fixture
def problem_input():
    return problem_file.parse_input(problem_file.INPUT_PATH)


def test_input_extant(sample_input, problem_input):
    """Checks that input parsing returns something."""
    assert sample_input is not None
    assert problem_input is not None


def test_sample_input_non_empty(sample_input):
    """Checks that the parsed sample input is not empty."""
    assert sample_input


def test_problem_input_non_empty(problem_input):
    """Checks that the parsed problem input is not empty."""
    assert problem_input


def test_part_1_sample(sample_input):
    """Checks part 1 against a known answer, using sample input."""
    assert problem_file.part_1(sample_input) == 0


def test_part_1_problem(problem_input):
    """Checks part 1 against a known answer, using problem input."""
    assert problem_file.part_1(problem_input) == 0


def test_part_2_sample(sample_input):
    """Checks part 2 against a known answer, using sample input."""
    assert problem_file.part_2(sample_input) == 0


def test_part_2_problem(problem_input):
    """Checks part 2 against a known answer, using problem input."""
    assert problem_file.part_2(problem_input) == 0
