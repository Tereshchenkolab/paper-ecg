from typing import List, Optional, Union

import numpy as np
import scipy.signal
import scipy.interpolate


def _findFirstPeak(signal: np.ndarray, minHeight: float = 0.3, prominence: float = 0.05) -> Optional[int]:
    peaks, _ = scipy.signal.find_peaks(signal, prominence=prominence, height=minHeight)
    if len(peaks) == 0:
        return None
    else:
        return peaks[0]

def _estimateFirstPeakLocation(
    signal: np.ndarray,
    interpolate: bool = True,
    interpolationRadius: int = 2,
    interpolationGranularity: float = 0.01
) -> Optional[float]:
    assert interpolationRadius >= 1

    index = _findFirstPeak(signal)
    if index is None:
        return None

    if interpolate:
        # Squeeze out a little more accuracy by fitting a quadratic to the points around the peak then finding the maximum
        start, end = index - interpolationRadius, index + interpolationRadius
        func = scipy.interpolate.interp1d(range(start, end + 1), signal[start:end + 1], kind='quadratic')
        newX = np.arange(start, end, interpolationGranularity)
        newY = func(newX)

        newPeak = newX[np.argmax(newY)]

        # <-- DEBUG -->
        # import matplotlib.pyplot as plt
        # plt.plot(range(start, end + 1), signal[start:end + 1])
        # plt.plot(newX, newY)
        # plt.show()

        return newPeak

    else:
        return index