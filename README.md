# Advent of Code 2024 - by Robert

This repo contains my solutions to the advent of code of last Christmas.

## Approach

[Last year](https://github.com/RobertoRoos/advent-of-code-2023) (I got about halfway) I felt I was repeating myself so much, so now I want to also maintain some shared code.
I imagine this could be classes for coordinates, queues, etc.

I also want to code to run more cleanly, so I think I'll make each solution a CLI program, with a .txt file as input.
And as some code is to be shared I'll need some unit tests to make sure everything keeps running.
I will keep my personalized challenge inputs out of this repo though.

## Setup

Python 3.11 or higher is required.

Prepare the repo by cloning and running `poetry install`.  
Alternatively, run:
```shell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

## Running

Run a specific solution like:
```shell
python -m advent_of_code.day_<nn> --part <1 or 2> <input file>
```

## Developing

### Tests

Tests are made with unittest.
Run all tests with:
```shell
python -m unittest
```

### Linting

Code linting is done through Black, Flake8 and isort.
