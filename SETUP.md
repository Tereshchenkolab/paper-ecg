[Project Homepage](README.md) / Setup Instructions (Unix)

# Setup Instructions

This guide takes you from a fresh install of macOS / Linux to having the project running. 

> **Note:** The only Linux distribution official supported by this guide is **Ubuntu**.

The steps involved are:

1. [Installing Pyenv](#install-pyenv)
1. [Installing Python `3.6.7`](#install-python-367)
1. [Setting up an environment](#set-up-an-environment)
1. [Installing dependencies](#install-dependencies)

This guide also explains:

- [How to run the application](#run-the-application)
- [Un-installation](#uninstalling)



## Install Pyenv

Pyenv is the best tool for managing different Python versions and isolating dependencies.

1. Install Pyenv via appropriate means for your system

    - **macOS**: Follow the [installation instructions](https://github.com/pyenv/pyenv#installation) in the Pyenv GitHub repository.

    - **Linux**: Use the automatic installer:

        ```bash
        $ curl https://pyenv.run | bash
        ```
        > Read the [automatic installer documentation](https://github.com/pyenv/pyenv-installer)

        ***(Ubuntu) Tip:*** If `pyenv` fails because it couldn't find `zlib`, run: `sudo apt install zlib1g-dev`.

1. Configure your shell correctly:

    **macOS**

    1. Add these lines to `.zshrc`:
        ```bash
        eval "$(pyenv init -)"
        eval "$(pyenv virtualenv-init -)"
        ```
        This can be done automatically by running:
        ```bash
        echo 'eval "$(pyenv init -)"' >> ~/.zshrc
        echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
        ```

    **Linux**

    1. Add these lines to the top of `.profile`:

        ```bash
        export PYENV_ROOT="$HOME/.pyenv"
        export PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init --path)"
        ```

    2. Add these lines to `.bashrc`:
        ```bash
        eval "$(pyenv init -)"
        eval "$(pyenv virtualenv-init -)"
        ```
        This can be done automatically by running:
        ```bash
        echo 'eval "$(pyenv init -)"' >> ~/.bashrc
        echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
        ```

    3. Changes to `.profile` do not become active until you log out and log back in again (or restart), but can be applied to the current shell by running `source ~/.profile`.

        - Run `source ~/.profile`

            OR
        - Logout and login

            OR
        - Restart

    > ⚠️ Note: as of May 2021 there was discussion of further changes to the Pyenv environment setup, so run `pyenv init` or read the [environment configuration guide](https://github.com/pyenv/pyenv#basic-github-checkout) on the Pyenv Github for the most up to date information.



## Install Python 3.6.7

1. Install Python [build dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment).


1. Install Python 3.6.7 using `pyenv install` with custom options:
    ```bash
    env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.6.7
    ```

    In order for PyInstaller to work correctly, you need a complete Python installation, so you need to specify `--enable-shared`. 
    In general `pyenv install 3.6.7` is sufficient to install a Python version via `pyenv`.

    If you encounter any issues, check the Pyenv [troubleshooting guide](https://github.com/pyenv/pyenv/wiki/Common-build-problems).



## Set up an environment

1. Use `pyenv` to create a virtual environment for the project. 

    ```bash
    pyenv virtualenv 3.6.7 paper-ecg
    ```

2. Navigate to the project root directory (`.../paper-ecg/`) and assign the virtual environment you just created to the current directory (this automatically activates the environment).

    ```bash
    pyenv local paper-ecg
    ```

    Now, whenever this folder is the working directory in terminal, this environment will be used.
    Test this out by running:

    ```bash
    > python --version
    3.6.7
    ```



## Install dependencies

Use `pip install` to install required dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> ⚠️ This may take several minutes



## Run the application

Navigate to the project root directory (`.../paper-ecg/`) and run `fbs run` to run the project.

***(Ubuntu) Tip:*** If `fbs run` fails because of `qt.qpa.plugin: Could not load the Qt platform plugin "xcb" ...` try re-installing `xcb`:

```bash
sudo apt install --reinstall libxcb-xinerama0
```



## Uninstalling

If you no longer want to have the `paper-ecg` virtualenv, you can delete it:

```bash
pyenv virtualenv-delete paper-ecg
```

If you wish to remove Python 3.6.7:
```bash
pyenv uninstall 3.6.7
```

If you would like to completely uninstall Pyenv:

- **macOS**: 
    ```bash
    brew uninstall pyenv
    ```

- **Linux**: 
    ```bash
    rm -rf $HOME/.pyenv
    ```
