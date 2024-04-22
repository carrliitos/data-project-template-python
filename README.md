# Project/Study Name
> [Author name goes here]

## Introduction

Sample project template with example connections to OCHIN-Epic Clarity.

Refer to this documentation to read more about 
[structuring our projects](https://docs.python-guide.org/writing/structure/).

## Installation

Download the project to your computer, navigate to the root folder and execute:

``` bash
python setup.py install
```

## Execution

To execute, navigate to the [src folder](./src) and run the following command:

``` bash
python main.py
```

## Structure

This project contains the following general sturcture:

- [data](./src/data): Datasets produced for cleaning, analysis, or distribution 
after execution of scripts. These are ignored by Git to protect any PHI.
- [data-raw](./src/data-raw): Incoming datasets that should be considered read-only.
These are ignored by Git to protect any PHI.
- [output](./src/output): Any documents or datasets intended for distribution from 
- [project_logs](./src/project_logs): Project logs created during development. 
Handled by Python's [logging module](https://docs.python.org/3/library/logging.html).
this project. These are ignored by Git to protect any PHI.
- [reports](./src/reports): Any rendered markdown/HTML documents that support the 
manipulation and analysis of datasets. These are ignored by Git to protect any 
PHI.
- [sql](./src/sql): SQL scripts to extract datasets. Before adding SQL scripts here, 
ensure no PHI is added in any clauses.
- [src](./src): Main source codes of interest.
- [venv](./src/venv): Virtual environment setup to hold packages/libraries needed to 
execute the project.