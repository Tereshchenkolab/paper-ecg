import os
import sys
from pathlib import Path
from typing import Sequence, Union
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.arraysetops import isin

import signal_loader

if os.name != 'posix':
    print("Julian doesn't understand Windows links :( sorry")

if len(sys.argv) < 3:
    print("Error! Too few arguments")
    exit(1)

firstPath = Path(sys.argv[1])
secondPath = Path(sys.argv[2])

assert firstPath.exists(), f"{firstPath} cannot be found!"
assert secondPath.exists(), f"{secondPath} cannot be found!"

firstECG = signal_loader.load(firstPath)
secondECG = signal_loader.load(secondPath)

numberOfComparisons = min(len(firstECG), len(secondECG))

fig, ax = plt.subplots(nrows=numberOfComparisons, ncols=1)
for index, row in enumerate(ax if isinstance(ax, (list, np.ndarray)) else [ax]):
    row.plot(firstECG[index])
    row.plot(secondECG[index])

plt.show()