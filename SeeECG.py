import os
import matplotlib.pyplot as plt
import numpy as np

import SignalLoader

if os.name != 'posix':
    print("Julian doesn't understand Windows links :( sorry")

prefix = "./data/1470/0000003"
letters = "UVWXY"

lead2Values = [] # Grab all the II leads

for letter in letters:
    leads = SignalLoader.load(prefix + letter + ".txt")

    leadCount, duration = leads.shape
    times = list(range(duration))

    lead2Values.append(leads[1]) # Grab all the II leads

plotNumber = 0


fig, ax = plt.subplots(nrows=5, ncols=1)
for row in ax:
    row.plot(times, lead2Values[plotNumber])
    plotNumber += 1

plt.show()