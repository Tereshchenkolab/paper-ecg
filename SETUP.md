[Project Homepage](README.md) /  Setup Instructions

# Setup Instructions

This guide takes you from a fresh install of Linux/MacOS/Windows to having the project running.

The steps involved are:

- Installing Python `3.6.7`
- Setting up an environment
- Loading dependencies

There are two different ways to install Python `3.6.7`:

1. Official Python Installer — This option is best for windows. ([jump](#1-official-python-installer))
1. `pyenv` — This option is best for Linux/macOS.([jump](#2-pyenv-macoslinux-only))

> ⚠️ This guide is designed to work in any shell, so the `>` is used to denote the shell prompt even thought your shell may have `%` or `$`.



## 1. Official Python Installer

### Install Python

Install Python `3.6.7` from the [python website](https://www.python.org/downloads/release/python-367/).

- [Click here](https://www.python.org/ftp/python/3.6.7/python-3.6.7-amd64.exe) to download Python 3.6.7 for Windows.

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
We will use this tool to keep all of the dependencies for the project separate from any other Python packages you may have installed.
Check out the [venv documentation](https://docs.python.org/3/library/venv.html)) for more information.

> 💡 Environments isolate different Python projects to prevent dependency conflicts.

Make sure when you run `python --version` you get `3.6.7`, or you are using the full path to the executable.

Create a virtual environment for the project. 

```
> python -m venv .env
```

#### Activating

In order to utilize the isolated environment you will need to activate the environment.
The activation command varies between operating systems and shells, and the correct command to use is given in the table below:

Platform|Shell          | Command to activate virtual environment
|-    |-                |-|
POSIX | bash/zsh        | `$ source .env/bin/activate`
|"    | fish            | `$ source .env/bin/activate.fish`
|"    | csh/tcsh        | `$ source .env/bin/activate.csh`
|"    | PowerShell Core | `$ .env/bin/Activate.ps1`
Windows | cmd.exe       | `C:\> .env\Scripts\activate.bat`
|"      | PowerShell    | `PS C:\> .env\Scripts\Activate.ps1`

##### 💡 Pro Tip

check the "Python > Env > Active Env In Current Terminal" box in the workspace settings or add this setting to `.vscode/settings.json`:

```
"python.terminal.activateEnvInCurrentTerminal": true,
```
    
#### Deactivating

After you have finished working on the project, and you want to return to your normal shell, you can deactivate the environment by running `deactivate` (works on all platforms).

### Install dependencies

To install all of the dependencies in your new environment, run:

`pip install -r requirements.txt`

> 💡 If pip complains about being out of date, just run `pip install --upgrade pip`

Now, running `fbs run` should build and run the project.



## 2. `pyenv` (macOS/Linux only)

`pyenv` is the most common tool for managing different Python versions.

### Install `pynenv`

#### macOS

Follow the [installation instructions](https://github.com/pyenv/pyenv#installation) on the `pyenv` GitHub.

#### Linux

Use the automatic [installer](https://github.com/pyenv/pyenv-installer):

```
$ curl https://pyenv.run | bash
```

**(Ubuntu) Tip:** If `pyenv` fails because it couldn't find `zlib`, run: `sudo apt-get install zlib1g-dev`.

**Note:** you may need to follow the instructions to add the `pyenv` setup to your `.bashrc`.

Then, follow the pre-requisites for your system in the [troubleshooting guide](https://github.com/pyenv/pyenv/wiki/Common-build-problems) (or try your luck and return here if `pyenv` fails).

### Download Python 3.6.7

```
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.6.7
```

For PyInstaller to work correctly, you need a complete Python installation, so you need to specify `--enable-shared`. 
In general `pyenv install 3.6.7` is sufficient to install a Python version via `pyenv`.

### Configure an environment

Use `pyenv` to create a virtual environment for the project. 

```
pyenv virtualenv 3.6.7 paper-ecg
```

Assign that virtual environment to the current directory (this automatically activates the environment).

```
pyenv local paper-ecg
```

Now, whenever this folder is the working directory in terminal, this environment will be used.
Test this out by running:

```
> python --version
3.6.7
```

### Install dependencies

```
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

> ⚠️ This may take several minutes

> 💡 If pip complains about being out of date, just run `pip install --upgrade pip`

Now, running `fbs run` should build and run the project.

**(Ubuntu) Tip:** If `fbs run` fails because of `qt.qpa.plugin: Could not load the Qt platform plugin "xcb" ...` try re-installing `xcb`:

    ```
    sudo apt-get install --reinstall libxcb-xinerama0
    ```
