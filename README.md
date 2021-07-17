# Paper ECG

An application for digitizing ECG scans. (OSU Capstone Project 2020-21)

See [ecgdigitize](https://github.com/Tereshchenkolab/ecg-digitize) for the library implementing the grid and signal digitization.

## Authors

- Natalie Coppa
- Julian Fortune
- Larisa Tereschenko (tereshch at ohsu.edu)

With help from:
- Kazi Haq
- Hetal Patel

## Overview

This application allows digitizing paper ECG image scans, such as this one:

![fullscan](https://user-images.githubusercontent.com/25210657/120732384-13bb9400-c49a-11eb-9913-5e99da0f8d53.png)

To produce digital signals, like these:

![fullscan-output](https://user-images.githubusercontent.com/25210657/120732452-3057cc00-c49a-11eb-8228-0d3f7cb31e78.png)


## Installation

Download the latest release [here](https://github.com/Tereshchenkolab/paper-ecg/releases/latest).


## User Guide

Read the user guide [here](USER-GUIDE.md)


## Contributing

Follow the set-up instructions:

- [macOS / Linux](SETUP.md)
- [Windows](SETUP-WINDOWS.md)

You should now have:

- Python 3.6.7
- Virtual environment
- All required packages

**Reminder**: Make sure your virtual environment is running! (this will happen automatically if you are using `pyenv`)

You can now run:

```
fbs run
```

Or, on Windows, you may need to run:

```
py -3.6 -m fbs run
```

This will start the interpreted version of the project.

### Build

In order to create an executable that can be distributed, run:

```
fbs build
```

Or, on Windows, you may need to run:

```
py -3.6 -m fbs build
```

This only builds an executable targeting the current OS (i.e., virtualization or multiple machines is necessary to produce builds for each OS).


## Contributing

View the [issues list](https://github.com/Tereshchenkolab/paper-ecg/issues) to see what tasks are available to work on.


## Dependencies

The project currently requires Python `3.6.7` to work with `fbs` (see [3.7 support issue](https://github.com/mherrmann/fbs/issues/61)).


## Build Notes

- Detailed [guide](https://gist.github.com/j9ac9k/1f2858ceb84d94b7643a6558967d954d) on PyQt + fbs + macOS building and releasing.
- [Dark mode doesn't work on macOS](https://github.com/pyinstaller/pyinstaller/issues/4627) when `frozen`.


## Capstone

See our sprint documents [here](scrum/README.md).

## Preprint to cite
Julian Fortune, Natalie Coppa, Kazi T Haq, Hetal Patel, Larisa G Tereshchenko. 
Digitizing ECG image: new fully automated method and open-source software code. 
medRxiv 2021.07.13.21260461; doi: https://doi.org/10.1101/2021.07.13.21260461

## Statistical validation code
see file digitizing_validation Stata code.do. See manuscript(peprint above) for the detailed description of statistical methods. 

