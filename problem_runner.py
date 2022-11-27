import argparse
import subprocess
import sys
import time
import tomli

from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.toml"


def get_config(config_path: Path = None) -> dict:
    with open(config_path, "rb") as config_file:
        config = tomli.load(config_file)
    return config


def benchmark(config: dict) -> None:
    """Tracks the time taken to run every problem registered as complete in the config file."""
    problems = config["benchmark"]["registered_problems"]
    year = config["setup"]["year"]

    start_time = time.perf_counter()
    last_split = start_time
    print(f"\nAdvent of Code {year} Benchmark\n")
    for day in problems:
        run_problem(day, "solve", 1, year=year, quiet=True)
        run_problem(day, "solve", 2, year=year, quiet=True)
        split = time.perf_counter()
        print(f"Day {day}: {'{:.3f}'.format(split - last_split)}")
        last_split = split
    print(f"\nTotal: {'{:.3f}'.format(time.perf_counter() - start_time)}")


def run_problem(
    day: int,
    mode: str,
    part: int,
    year: int,
    log_level: str = None,
    quiet: bool = False,
) -> None:
    """
    Runs a specified problem.
    """
    day_str = "{:0>2d}".format(day)
    folder_name = f"day_{day_str}"
    file_name = f"aoc_{year}_day_{day_str}.py"
    args = ["python3", f"{folder_name}/{file_name}", mode, str(part)]
    if log_level is not None:
        args.extend(["--log-level", f"{log_level}"])
    visible = subprocess.DEVNULL if quiet else None
    subprocess.run(args, stdout=visible)


def cli(config):
    year = config["setup"]["year"]
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int, choices=range(101))
    parser.add_argument("mode", type=str, choices={"check", "solve"})
    parser.add_argument("part", type=int, choices={1, 2})
    parser.add_argument(
        "--log-level",
        type=str,
        required=False,
        choices={"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"},
    )
    parser.add_argument("--quiet", required=False, action="store_true")
    args = parser.parse_args()
    run_problem(
        args.day,
        args.mode,
        args.part,
        year,
        log_level=args.log_level,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    config = get_config(CONFIG_FILE)
    if len(sys.argv) == 1:
        benchmark(config)
    else:
        cli(config)
