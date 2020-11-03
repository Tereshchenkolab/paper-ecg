[Project Homepage](README.md) /  Setup Instructions

# Setup Instructions

This guide takes you from a fresh install of Linux/MacOS/Windows to having the project running. 

The steps involved are:

- Installing Python `3.6.7`
- Setting up an environment
- Loading dependencies

However, there are three different ways to accomplish this:

1. Official Python Installer ([jump](#1-official-python-installer))
1. Anaconda ([jump](#2-anaconda))
1. `pyenv`([jump](#3-pyenv-macoslinux-only))

### Which one is right for me?

Here is a recommendation flow chart to make the decision easy:

```
    +-----------------+          +--------------+
    |   Do you use    |          |  Do you use  |
--->|   python for    +-- yes -->+   Windows?   +-- yes --> [ Anaconda ]
    | other projects? |          |              |
    +--------+--------+          +------+-------+
             |                          |
             no                         no
             |                          |
             v                          v
    [ Python Installer ]             [ pyenv ]
```

**Note**: Anaconda is available for Windows/Linux/macOS, and there is a [windows port of `pyenv`](https://github.com/pyenv-win/pyenv-win) available.



## 1. Official Python Installer

### Install Python

Install Python `3.6.7` from the [python website](https://www.python.org/downloads/release/python-367/).

You can verify that the install was successful with:

```
$ python --version
3.6.7
```

If this returns `2.7.X`, try `python3 --version`. 
If that works, use `python3` in place of `python` for the rest of instructions. 

If neither of those works you will need to specify the full path to the Python 3.6.7 executable:

```
$ /path/to/python3.6.7 --version
3.6.7
```

### Create an environment

Python comes bundled with an environment manager, `venv` (not to be confused with `virtualenv` or `pyenv`). 
We will use this tool to package all of the dependcies for the project in a locally.
Check out the [venv documentation](https://docs.python.org/3/library/venv.html)) for more information.

```
💡 Environments isolate different Python projects to prevent dependency conflicts.
```

Make sure when you run `python --version` you get `3.6.7`, or you are using the full path to the executable.

Run `venv <environment name>` to create a virtual envirnonment for the project. 

```
python -m venv environment
```

#### Activating / deactivating

In order to utilize the isolated environment you will need to activate the environemnt.

...

### Install dependencies

...




## 2. Anaconda

### Install Miniconda (or Anaconda)

"Miniconda" is the minimal version of Anaconda, a data science bundle. 
Miniconda comes with Python and `conda`, the hybrid package/environment manager.
The Python version will not be `3.6.7` but that's ok, because we can use `conda` to set up a development environment for the project.
Anaconda comes with a bunch of extra things that aren't necessary, but if you want the full experience you can install Anaconda instead.

#### Windows

Download and run the installation manager from the [install](https://docs.conda.io/en/latest/miniconda.html) page.

You can alternatively install the full version of Anaconda from the [Anaconda website](https://www.anaconda.com/products/individual).

Verify the installation was successful by running `conda --version`.

#### MacOS/Linux

Follow the installation instructions for [macOS](https://conda.io/projects/conda/en/latest/user-guide/install/macos.html) and [Linux](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html).

Verify the installation was successful by running `conda --version`.

To prevent conda from taking `python` and `python3` hostage globally, run:

```
conda config --set auto_activate_base false
```

### Set up an environment

...

### Install dependencies

...




## 3. `pyenv` (macOS/Linux only)

`pyenv` is the most common tool for managing different Python versions.

### Install `pynenv`

...

### Download Python 3.6.7

...

### Configure an environment

Use the built-in module `venv` to create a virtual envirnonment for the project ([venv documentation](https://docs.python.org/3/library/venv.html)). 

```
python -m venv environment
```

...

### Install dependencies

```
pip install -r requirements.txt
```

...
