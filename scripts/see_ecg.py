import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import sys

import signal_loader

if os.name != 'posix':
    print("Julian doesn't understand Windows :( sorry")

if len(sys.argv) < 2:
    print("Error!")
    print(f"Usage: python {sys.argv[0]} PATIENT_ID")
    exit(1)

file = sys.argv[1]

# duration = 0
# lead2Values = [] # Grab all the II leads

leads = signal_loader.load(file)

leadCount, duration = leads.shape
times = list(range(duration))

plotNumber = 0

fig, ax = plt.subplots(nrows=leadCount, ncols=1)
for row in ax:
    # row.title.set_text(name)
    row.plot(times, leads[plotNumber])
    plotNumber += 1

plt.show()