# Phys601: Computational Recitation

* Prof. Maurik Holtrop

Python notebooks and code for the computational recitation (Phys 601 & 602) at 
the University of New Hampshire. The aim is to learn how to solve the problems 
that come up in your physics courses numerically, and to become comfortable setting up 
that kind of work on your own. The recitation is a working session: bring your questions, 
bring your own computer, and bring problems from your other courses.

## Getting started

There are two ways to run the notebooks.

**In the browser, no installation.** Open any notebook in Google Colab by replacing
`https://github.com/` in its address with `https://colab.research.google.com/github/`.
To keep your changes, save a copy to your Google Drive. Try it with the first notebook:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mholtrop/Phys601/blob/master/Notebooks/00_Intro_Notebooks.ipynb)

**On your own computer (recommended).** We suggest PyCharm together with a conda environment from Miniforge.

1. First Install [Miniforge](https://github.com/conda-forge/miniforge) and then [PyCharm](https://www.jetbrains.com/pycharm/).
   PyCharm's core version, including Jupyter notebook support, is free. Students can get the Pro version free
   through the [JetBrains Student Pack](https://www.jetbrains.com/community/education/#students).
2. In PyCharm, clone this repository (`https://github.com/mholtrop/Phys601.git`) with "Clone Repository"
   on the welcome screen.
3. Open a terminal in the `Phys601` folder (on Windows, use the "Miniforge Prompt") and create the
   course environment from the included [environment.yml](environment.yml):
   ```bash
   conda env create -f environment.yml
   ```
4. Back in PyCharm, set the project interpreter: choose **Conda** and select the existing `phys601`
   environment. (PyCharm may suggest uv or a new virtualenv instead; don't take that default.)

If you prefer not to use PyCharm, JupyterLab works on its own:

```bash
git clone https://github.com/mholtrop/Phys601.git
cd Phys601
conda env create -f environment.yml
conda activate phys601
jupyter lab
```

If you do not have `git`, use the green "Code" button above and choose "Download ZIP".
If any of this does not work for you, bring your laptop to recitation. Getting set up is part of the course.

## Where to start

Begin with `Notebooks/00_Intro_Notebooks` and the two `00_python_tutorial` notebooks, then continue
in numerical order. Notebooks starting with "A" are advanced; those starting with "E" are extras.
[Notebooks/README.md](Notebooks/README.md) describes each one.

| Folder | Contents |
|---|---|
| `Notebooks` | The main sequence of notebooks |
| `Exercises` | Practice problems that go with the main notebooks |
| `Advanced` | Larger examples, with less step-by-step explanation |
| `QM_Notebooks` | Numerical quantum mechanics: bound states, time evolution, tunneling |
| `Special_Relativity` | Minkowski space-time diagram tools (used in Phys 505) |
