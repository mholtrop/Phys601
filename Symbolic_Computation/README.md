# Symbolic Computation

Notebooks on doing algebra and calculus symbolically: exact results instead of numbers. This is useful in general and a good 
way to check your own work. You can use this for
deriving equations of motion, doing integrals and series expansions, solving linear algebra problems exactly, and
checking hand calculations before you turn them into numerical code.

| Notebook | Contents |
|---|---|
| `SG1_Intro_to_Sage` | Introduction to SageMath: exact arithmetic, simplification, solving equations, calculus, normal modes, differential equations, Lagrangian mechanics, plotting, and moving results to NumPy and LaTeX |
 | `SY1_Sympy_introduction` | A plain Python library that covers similar ground with somewhat less elegant input methods. |

## Running Sage

[SageMath](https://www.sagemath.org) is a large system and is not part of the standard `phys601` environment. There are several
ways to use it. The Sympy library *is* already included in the `phys601` environment, since it is more direct Python.

**In the browser, no installation.**
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mholtrop/Phys601/blob/master/Symbolic_Computation/SG1_Intro_to_Sage.ipynb)
The first code cell of the notebook installs Sage into the Colab session with pip
([passagemath](https://github.com/passagemath/passagemath), a pip-installable version of Sage). This takes a few minutes
and has to be repeated for each new Colab session. Colab may warn that it does not recognize the SageMath kernel;
it then runs the notebook with Python, which works. For a single quick calculation, the
[SageMathCell](https://sagecell.sagemath.org) web page needs no setup at all.

**On Linux or macOS.** Install Sage from conda-forge in its own environment. Sage pins many of its dependencies, so
keep it separate from `phys601`. The download is large.

```bash
conda create -n sage sage jupyterlab
conda activate sage
cd Phys601/Symbolic_Computation
jupyter lab
```

In JupyterLab, choose the **SageMath** kernel. To use PyCharm instead, select the `sage` conda environment as the
interpreter. PyCharm then runs the notebook with a Python kernel, and the first code cell of the notebook switches
Sage on.

**On Windows.** Sage does not run natively on Windows. Install the Windows Subsystem for Linux (WSL) with Ubuntu,
following the [Sage installation guide](https://doc.sagemath.org/html/en/installation/index.html), install Miniforge
inside Ubuntu, and then follow the Linux instructions above. If that is more than you want to do, use Colab.
