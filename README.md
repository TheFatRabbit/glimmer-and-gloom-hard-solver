# Glimmer and Gloom Hard Solver
A solver for Hard difficulty of the Glimmer and Gloom minigame on Flight Rising

- ### <b>This repository is NOT ACTIVELY DEVELOPED! For more efficient treasure from Glimmer and Gloom, see [my Very Hard difficulty solver](https://github.com/TheFatRabbit/glimmer-and-gloom-very-hard-solver)!</b>

Upon pressing a button or a customizable hotkey, the solver will search specific bounds for occurrences of both glimmer and gloom tiles and calculate the clicks required to solve the board from its curret state. The program will then overlay an indicator onto all tiles that need to be clicked in order to solve the board.

---

# Setup
Clone this repository. See this link if you need help: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository

# Requirements
- Python (https://www.python.org/downloads/)
    - Pip (https://pip.pypa.io/en/stable/installation/) (should be preinstalled with Python)
    - Libraries:
        - Navigate to the project directory (in Command Prompt, type `cd <folder path>`)
        - Type the following command: `pip install -r requirements.txt`
You should now be ready to set up the `config.json` file

# Config
- In `config.json` set the following:
    - Preferred hotkey (must be a valid hotkey in the `keyboard` package)
    - Screen bounding box in the form (x<sub>1</sub>, y<sub>1</sub>, x<sub>2</sub>, y<sub>2</sub>) following the image below
        - I suggest using MPos (https://sourceforge.net/projects/mpos/) to find your mouse position
<p align="center"><img height="300" src="https://i.imgur.com/Ypx7hfc.png"></p>

# Screenshots
- In the same environment as the one you will play G&G in, take a screenshot of the glimmer and gloom tiles, while leaving some space on each side. Name them `glimmer.png` and `gloom.png` and replace the current example files. If the proportions of your game are vastly different from mine, you may find smaller images lead to more reliable detection.

**You should be ready to run the program!**

To run the program without the command prompt, run `hard_solver.pyw`. It will terminate when you close the gui.
If you encounter any problems, create an issue.
