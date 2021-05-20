import os
import matplotlib.pyplot as plt
import numpy as np
import glob
import sys

import SignalLoader

if os.name != 'posix':
    print("Julian doesn't understand Windows :( sorry")

if len(sys.argv) < 2 or not sys.argv[1].isdigit():
    print("Error!")
    print(f"Usage: python {sys.argv[0]} PATIENT_ID")
    exit(1)

prefix = f"./data/{sys.argv[1]}"

duration = 0
lead2Values = [] # Grab all the II leads

for file in sorted(glob.glob(f"{prefix}/*.txt")):
    leads = SignalLoader.load(file)

    leadCount, duration = leads.shape
    times = list(range(duration))

    name = file.split('/')[-1]

    lead2Values.append((name, leads[1])) # Grab all the II leads

plotNumber = 0

fig, ax = plt.subplots(nrows=len(lead2Values), ncols=1)
for row in ax:
    name, signal = lead2Values[plotNumber]
    row.title.set_text(name)
    row.plot(times, signal)
    plotNumber += 1

plt.show()