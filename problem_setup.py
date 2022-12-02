import argparse
import requests
import shutil
import tomli

from hashlib import md5
from pathlib import Path


PARENT_FOLDER = Path(__file__).parent
CONFIG_FILE = PARENT_FOLDER / "config.toml"
CONFIG_SECRET_FILE = PARENT_FOLDER / "config_secret.toml"
TEMPLATE_FOLDER = PARENT_FOLDER / "templates"
TEMPLATE_FILES = {
    "problem": TEMPLATE_FOLDER / "aoc_template_problem.py",
    "test": TEMPLATE_FOLDER / "aoc_template_test.py",
    "sample": TEMPLATE_FOLDER / "aoc_template_sample.txt",
    "input": TEMPLATE_FOLDER / "aoc_template_input.txt",
    "scratch": TEMPLATE_FOLDER / "aoc_template_scratch.py",
}
CACHE_FOLDER = PARENT_FOLDER / "aoc_cache"
CACHE_CANARY_FILE = CACHE_FOLDER / "canary.txt"


def _download_problem_input(day: int, year: int, cookie: str = None) -> str:
    if cookie is None:
        cookie = _read_config(CONFIG_SECRET_FILE)["auth"]["cookie"]
    if not cookie:
        return "No session cookie found. You'll need to copy the input manually."
    input_url = f"https://adventofcode.com/{year}/day/{day}/input"
    headers = {
        "User-Agent": "https://github.com/phildavis17/aoc_helper"
    }
    s = requests.Session()
    s.cookies.set("session", cookie)
    input_text = s.get(input_url, headers=headers).text
    return input_text


def _write_input_to_file(file_path: Path, input_text: str) -> None:
    with open(file_path, "w") as input_file:
        input_file.write(input_text)


def _get_hash_key(cookie: str, day_str: str):
    """
    Returns a hashed string of the session cookie and the day string.
    
    This hash is used as the filename of a cached input file
    to avoid collisions if the cookie has changed.
    """
    return md5(bytes(cookie + day_str, "utf-8")).hexdigest()

def _write_canary(cookie: str) -> None:
    with open(CACHE_CANARY_FILE, "w") as canary:
        canary.write(cookie)

def _clear_cache() -> None:
    for cache_file in CACHE_FOLDER.iterdir():
        Path.unlink(cache_file)

def _canary_is_current(cookie: str) -> bool:
    with open(CACHE_CANARY_FILE, "r") as canary_file:
        canary_cookie = canary_file.read().strip()
        return canary_cookie == cookie


def get_input_data(day_str: str, year: int, cookie: str) -> str:
    """
    Returns input data from cached input file.
    If cached input does not exist, create it, and read from it.
    """
    if not Path.exists(CACHE_FOLDER):
        Path.mkdir(CACHE_FOLDER, parents=True)
    if not (Path.exists(CACHE_CANARY_FILE) and _canary_is_current(cookie)):
        _clear_cache()
        _write_canary(cookie)
    hash_key = _get_hash_key(cookie, day_str)
    cached_input_file = CACHE_FOLDER / f"{hash_key}.txt"
    if not Path.exists(cached_input_file):
        input_data = _download_problem_input(int(day_str), year, cookie)
        _write_input_to_file(cached_input_file, input_data)
    with open(cached_input_file, "r") as input_file:
        input_data = input_file.read().strip()
    return input_data


def setup_input_file(day_str: str, year: int, input_path: Path, cookie: str = None):
    input_text = get_input_data(day_str, year, cookie)
    _write_input_to_file(input_path, input_text)


def _format_day_string(day: int) -> str:
    return "{:0>2d}".format(day)


def build_template_file_names(day_str: str, year: int) -> dict:
    file_name_base = f"aoc_{year}_day_{day_str}"
    problem_file_names = {
        "problem": f"{file_name_base}.py",
        "test": f"{file_name_base}_test.py",
        "sample": f"{file_name_base}_sample.txt",
        "input": f"{file_name_base}_input.txt",
        "scratch": "scratch_1.py",
    }
    return problem_file_names


def populate_problem_folder(problem_folder: Path, file_names: dict) -> None:
    Path.mkdir(problem_folder, parents=True)
    for role, template_file in TEMPLATE_FILES.items():
        if role == "problem":
            continue
        problem_file = problem_folder / file_names[role]
        shutil.copy(template_file, problem_file)


def write_problem_file(
    problem_folder: Path,
    problem_file_name: str,
    intro_comment: str,
) -> None:
    with open(problem_folder / problem_file_name, "w") as problem_file, open(
        TEMPLATE_FILES["problem"], "r"
    ) as template:
        problem_file.write(intro_comment)
        problem_file.write(template.read())


def _build_intro_comment(day_string: str, config: dict) -> str:
    introductory_comment = f"# Advent of Code {config['year']}\n# Day {day_string}\n"
    if config["author"]:
        introductory_comment += f"# {config['author']}\n"
    introductory_comment += "\n"
    return introductory_comment


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int, help="the number of the problem to set up.")
    arguments = parser.parse_args()
    day = arguments.day
    if not 0 <= day < 100:
        raise ValueError(f"{day} is not a usable day number")
    main(arguments.day)


def _read_config(toml_path: Path):
    with open(toml_path, "rb") as toml_file:
        return tomli.load(toml_file)


def main(day: int):
    config = _read_config(CONFIG_FILE)["setup"]
    year = config["year"]
    cookie = _read_config(CONFIG_SECRET_FILE)["auth"]["cookie"]
    day_str = _format_day_string(day)
    intro_comment = _build_intro_comment(day_str, config)
    problem_folder = PARENT_FOLDER / f"day_{day_str}"
    file_names = build_template_file_names(day_str, year)
    populate_problem_folder(problem_folder, file_names)
    write_problem_file(problem_folder, file_names["problem"], intro_comment)
    setup_input_file(day_str, year, problem_folder / file_names["input"], cookie)


if __name__ == "__main__":
    raise SystemExit(cli())
    

