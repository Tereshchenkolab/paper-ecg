[Project Homepage](README.md) /  Setup Instructions

# Setup Instructions

This guide takes you from a fresh install of Linux/MacOS/Windows to having the project running.

The steps involved are:

- Installing Python `3.6.7`
- Setting up an environment
- Loading dependencies

However, there are three different ways to accomplish this:

1. Official Python Installer — This option is best for windows. ([jump](#1-official-python-installer))
1. `pyenv` — This option is best for Linux/macOS.([jump](#2-pyenv-macoslinux-only))

> ⚠️ This guide is designed to work in any shell, so the `>` is used to denote the shell prompt even thought your shell may have `%` or `$`.



## 1. Official Python Installer

### Install Python

Install Python `3.6.7` from the [python website](https://www.python.org/downloads/release/python-367/).

You can verify that the install was successful with:

```
> python --version
3.6.7
```

If this returns `2.7.X`, try `python3 --version`. 
If that works, use `python3` in place of `python` for the rest of instructions. 

If neither of those works you will need to specify the full path to the Python 3.6.7 executable:

```
> /path/to/python3.6.7 --version
3.6.7
```

### Create an environment

Python comes bundled with an environment manager, `venv` (not to be confused with `virtualenv` or `pyenv`). 
We will use this tool to package all of the dependcies for the project in a locally.
Check out the [venv documentation](https://docs.python.org/3/library/venv.html)) for more information.

> 💡 Environments isolate different Python projects to prevent dependency conflicts.

Make sure when you run `python --version` you get `3.6.7`, or you are using the full path to the executable.

Create a virtual envirnonment for the project. 

```
> python -m venv .env
```

#### Activating

In order to utilize the isolated environment you will need to activate the environemnt.
The activation command varies between operating systems and shells, and the correct command to use is given in the table below:

Platform|Shell| Command to activate virtual environment
|-|-|-|
POSIX | bash/zsh | `$ source <venv>/bin/activate`
|"| fish | `$ source <venv>/bin/activate.fish`
|"| csh/tcsh | `$ source <venv>/bin/activate.csh`
|"| PowerShell Core | `$ <venv>/bin/Activate.ps1`
Windows | cmd.exe | `C:\> <venv>\Scripts\activate.bat`
|"| PowerShell | `PS C:\> <venv>\Scripts\Activate.ps1`
    
#### Deactivating

After you have finished working on the project, and you want to return to your normal shell, you can deactivate the environment by running `deactivate` (works on all platforms).

### Install dependencies

To install all of the dependencies in your new environment, run:

`pip install -r requirements.txt`

**Bonus**:If pip complains about being out of date, just run `pip install --upgrade pip`

Now, running `fbs run` should build and run the project.



## 2. `pyenv` (macOS/Linux only)

`pyenv` is the most common tool for managing different Python versions.

### Install `pynenv`

Follow the [installation instructions](https://github.com/pyenv/pyenv#installation) on the `pyenv` GitHub.

### Download Python 3.6.7

```
pyenv install 3.6.7
```

The `.python-version` in the repo already specifies Python `3.6.7`.
Make sure that is working by running:

```
> python --version
3.6.7
```

If that doesn't work, try setting the version of Python in the repo folder manually:

```
pyenv local 3.6.7
```

### Configure an environment

Use `pyenv` to create a virtual envirnonment for the project ([venv documentation](https://docs.python.org/3/library/venv.html)). 

```
pyenv virtualenv 3.6.7 paper-ecg
```

Use pyenv to automatically activate the environment in this directory:

```
pyenv local paper-ecg
```

Now, whenever this folder is the working directory in terminal, this environment will be used.

### Install dependencies

```
pip install -r requirements.txt
```

Now, running `fbs run` should build and run the project.
