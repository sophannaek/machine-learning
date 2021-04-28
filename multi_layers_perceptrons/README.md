# **CECS 550 Project 2 - Multi Layer Perceptron**
## **Team**: *Classy Fire*
### **Team Members**: [Sophanna Ek](https://github.com/sophannaek), [Melissa Hazlewood](https://github.com/melissahazlewood), [Rowan Herbert](https://github.com/RLHerbert), [Dennis La](https://github.com/depla)

#
## **Project Contents** - File Hierarchy
- `ml_perceptron/`
  - `src/`
    - `data.py`
      - Contains methods for retrieving the vectors needed for the training and validation of the program.
    - `main.py`
      - The entry point to the program.
    - `mlp.py`
      - Contains the *multi layer perceptron* `mlp` class and handles its instantiation as well as forward and backward propogation of training vectors and error respectively.
    - `test.py`
      - Contains unit tests for the project.
    - `res/`
      - `data.txt`
        - Contains the raw data vectors.

#
## Prerequisites
- A basic understanding of programming and terminal emulator know how.
- An installation of `Python3` (or `Python`) which can be found [here](https://www.python.org/downloads/).
- A Python package manager such as [pip](https://pypi.org/project/pip/). It can be installed by following the instructions [here](https://pip.pypa.io/en/stable/installing/).
- The [NumPy](https://numpy.org) package for Python. It can be installed with `pip` by running the terminal command `pip install numpy`.

#
## Usage
Cloning from GitHub:
- You can `Git` clone the GitHub repo with `git clone https://github.com/RLHerbert/ml_perceptron.git`.

Follow these steps to run the program:
1. Navigate to the `ml_perceptron` folder in your terminal emulator of choice.
2. Run Python3 by typing and entering `Python3 src/main.py` in your terminal.
   - Alternatively, if you wish to save the resulting output you may enter `Python3 src/main.py > [output file]` on Linux/MacOS terminals and Windows PowerShell.

#
## Features

This project features a multilayer perceptron classifier which utilizes forward propogation training and backward propogation error correction to classify the provided data set.