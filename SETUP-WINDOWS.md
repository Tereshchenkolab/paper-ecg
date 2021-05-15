[Project Homepage](README.md) / Setup Instructions (Windows)

# Setup Instructions (Windows)

This guide takes you from a fresh install of Windows to having the project running.

The steps involved are:

1. [Installing Python 3.6.7](#1-install-python-3-6-7)
1. [Installing dependencies](#2-installing-dependencies)


## 1. Install Python 3.6.7

1. Install Python `3.6.7` via official installer. 

    - [Click here](https://www.python.org/ftp/python/3.6.7/python-3.6.7-amd64.exe) to download the installer.

        *OR*
    - View other installation options on the [python website](https://www.python.org/downloads/release/python-367/).



1. Verify that the install was successful with:

    ```
    > py -3.6 --version
    3.6.7
    ```

## 2. Install Dependencies

There are two options:

1. Install dependencies globally
1. Create an environment

If you are not a Python power user, it is recommended *not to use a virtual environment* (since it is complicated), and use Option 1 — Install dependencies globally. 

If you have mutliple Python projects and want to keep the dependencies isolated, you may want to use a virtual environment. Check out the [documentation](https://docs.python.org/3/library/venv.html)) for more information.

### Option 1 — Installing dependencies globally

Navigate to the project root directory (`...\paper-ecg\`) and run:

```
py -3.6 -m pip install -r requirements.txt
```

> 💡 If pip complains about being out of date, just run `py -3.6 -m pip install --upgrade pip`.

Now, running `fbs run` should build and run the project. If that doesn't work, try `py -3.6 -m fbs run`.




### Option 2 — Create an environment (Optional) and install dependencies

Create a virtual environment for the project. 

```
> py -3.6 -m venv .env
```

##### Activating

In order to utilize the isolated environment you will need to activate the environment.
The activation command varies between operating systems and shells, and the correct command to use is given in the table below:

Shell          | Command to activate virtual environment
|-                |-|
cmd.exe       | `C:\> .env\Scripts\activate.bat`
PowerShell    | `PS C:\> .env\Scripts\Activate.ps1`



##### 💡 Pro Tip for VSCode

Check the "Python > Env > Active Env In Current Terminal" box in the workspace settings or add this setting to `.vscode\settings.json`:

```
"python.terminal.activateEnvInCurrentTerminal": true,
```



#### Install dependencies

To install all of the dependencies in your new environment, run:

`pip install -r requirements.txt`

> 💡 If pip complains about being out of date, just run `pip install --upgrade pip`.

Now, running `fbs run` should build and run the project.



#### Deactivating

After you have finished working on the project, and you want to return to your normal shell, you can deactivate the environment by running `deactivate` (works on all platforms).



