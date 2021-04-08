import numpy as np

from .model.EcgModel import EcgModel
from .ECGToolkit.Common import *


def convertECGLeads(ecgData: EcgModel) -> np.ndarray:

    # 1. Map all lead images to signal data
    # 1.1 Check that not all( is None) -> Failure

    # 2. Map leads to grid size estimates
    # 2.1 Average them in each direction

    # 3. Estimate the sampling period (handle if this is None)

    # 3. Zero pad all signals on the left based on their start times and the samplingPeriod
    # take the max([len(x) for x in signals]) and zero pad all signals on the right

    # (should already be handled by (3)) Replace any None signals with all zeros

    pass