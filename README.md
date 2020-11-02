# Paper ECG
OSU Capstone Project 2020-21 - Natalie &amp; Julian

## Install Python 3.6.7

The `fbs` project is target to Python `3.6.7`. We might be able to use any `3.5-3.7`.

There are a few different ways to do this:


### 1. Python Installer

Install Python `3.6.7` from the python website.

If you want to use this version of Python globally make sure when you run `python --version` you get `3.6.7`.

Otherwise, you can use `python -m venv` to create a virtual envirnonment for the project ([venv documentation](https://docs.python.org/3/library/venv.html)). 

```
/path/to/python3.6.7 -m venv pyenvironment
```

**NOTE:** Make sure to use the full path to the Python 3.6.7 executable if it is not your global Python.


### 2. Anaconda

Install the minimal version of Anaconda, "Miniconda".

#### MacOS/Linux

<install instructions>

To prevent `python` and `python3` from being overwritten, run:

```
conda config --set auto_activate_base false
```

### 3. `pyenv` (macOS/Linux only)

`pyenv` is a sweet way to manage different Python versions.

#### Download Python 3.6.7

## Install Dependencies
