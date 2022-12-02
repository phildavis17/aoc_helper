# Advent of Code Helper

## What is this?
The intent of this repo is to provide a convenient, orderly framework for solving AoC problems using Python. It lets you:
 - Easily create a new folder with template files for each day's problem, and automatically download that day's input
 - Run your solution code using either sample input or the full problem input
 - Time your completed solutions to see how efficient your code is
 - Apply formatting and basic tests
 - Do all this using a convenient command runner interface


## Getting Set Up

### Install just
You'll need to install [just](https://github.com/casey/just#just), which is used as a command runner. It provides a convenient and consistent interface for performing the various AoC tasks this repo can do.

### Install Python Dependencies
This repo used a handful of common python libraries, which you can install by running `$ pip install -r requirements.txt`

### Setup `config.toml`
This config file needs to be populated with the following information:
 - Year - the year of AoC you are working on. **Note**: this repo does not support working on multiple years of AoC at once. 
 - Author - A name to include in the introductory comments in the problem template. This is optional.
 - Registered Problems - A list of problems that have been completed. Problems registered will be run by the time-trial script.

### Setup `config_secret.toml`
This repo expects there to be a file called `config_secret.toml`, which can be created easily by running `$ just init-secret-config`, and copying your AoC session cookie into the file. You can find this cookie in your browser's developer tools once you've logged in to the AoC site. **Note**: This file is not tracked by git, so you don't need to worry about pushing your credentials to Github.

## Usage
### TLDR
run `$ just` to see a list of things the justfile can do.

### Setting Up a New Problem
`$ just setup 1`

This will write 5 files to the newly created folder:
 - The Problem file - A python file where you can code up that day's solution.
 - The Sample file - A text file intended for sample input provided in the description of that day's problem.
 - The Input file - A text file that will be automatically populated with the full input of that day's problem.
 - The Test file - A python file containing basic tests. 
 - The scratch file - An empty python file you can use to experiment with. **Note**: the .gitignore includes files that start with 'scratch', so by default, these files are not tracked.

### Coding Your Solution
In the problem template, there are 4 functions ready for you to code up:
- `parse_input` - This reads the raw input file, and formats the data however you see fit.
- `part_1` - This returns a solution for part 1 of the day's puzzle.
- `part_2` - This returns a solution for part 2 of the day's puzzle.
- `run_direct` - This function is executed if the problem file is run directly, rather than through the `just` interface. This is useful for quick tasks like checking to see that your input is formatted the right way, or chasing down a bug. 

### Checking Your Work
Advent of Code problems usually include a small set of sample data along with the correct answer to the problem using that data as an input. Copying that sample data to the day's `"..._sample.txt"` file will let you use that sample input to check against as you work on your solution. To do this using the `just` interface, type `'just check '` followed by the day's number, and either 1 or 2, depending on which part of the day's puzzle you want to check.

For example, `$ just check 1 2` will run part 2 of day 1, using sample input.

### Solving
Solving works just like checking, but it will use the full puzzle input instead of the sample input.

`$ just solve 2 1` will run part 1 of day 2 using the full input.

### Benchmark
As you complete daily puzzles, add each day's number to the list of registered problems in `config.toml`. 
Running `$ just benchmark` will execute both parts of every registered problem with a timer running, and show you how long it took to run all your solutions, with splits for each day.


### Running Tests
`$ just test 1` will run tests on problem 1. `$ just test-all` will run tests in all problem folders.

### Formatting
You can enter `$ just black` to run black on your code. `$ just black-check` will show the changes black *would* make, if you just want to see what black has to say. 

### Cleaning Up and Starting Over
`$ just remove 1` will remove the folder for problem 1. `$ just reset 1` will remove the folder and set it up again.

## Technical Stuff

### Notes on the Problem Template
The output of `parse_input` is passed to `part_1` and `part_2` by the code running script. If these functions are renamed, or if they are made to return something that doesn't fit this flow, the `just` interface will stop working as expected.

### Notes on Tests
The tests included in the template are very basic. There are a few tests to guard against obvious faults in input parsing, and then 4 tests that check your `part_1` and `part_2` code using both the sample and full inputs. **Note** you'll need to replace the 0s in the tests with the correct answers, once you know them.
The `just` interface doesn't do anything sophisticated with the tests, so you can add, remove, or rename whatever you like in here without disrupting much.

### Logging
By default, code will be run with a logging level of `WARNING`, but `$ just debug 2 1` will run part 1 of day 2 using sample input with the logging level set to `DEGBUG`. This allows you to include logging statements that are helpful while working through a problem, but won't clutter your output when you're solving.

### Caching
When first downloaded, problem inputs are written to a local cache folder. As long as the session cookie has not changed, problem inputs will be read from this local cache instead of the AoC website when `$ just setup` is run. 