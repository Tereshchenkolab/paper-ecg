import functools
from pathlib import Path

import numpy as np

from model.EcgModel import Ecg
import digitize
from digitize import common, grid, signal
from digitize.signal import detection as signal_detection
from digitize.signal import extraction as signal_extraction
from digitize.grid import detection as grid_detection
from digitize import visualization


LEAD_ORDER = {
    leadID: i for i, leadID
    in enumerate(["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"])
}


def convertECGLeads(ecgData: Ecg):

    # TODO: Make parameters
    signalDetectionMethod = functools.partial(signal_detection.mallawaarachchi, useBlur=True)
    signalExtractionMethod = signal_extraction.naïveHorizontalScan

    leads = common.zipDict(ecgData.leads)

    extractSignal = functools.partial(signal.extractSignalFromImage, detectionMethod=signalDetectionMethod, extractionMethod=signalExtractionMethod)
    extractGrid   = grid.extractGridFromImage

    # Map all lead images to signal data
    signals = common.mapList(leads, lambda pair: (pair[0], extractSignal(pair[1].roiData.pixelData)))

    # If all signals failed -> Failure
    if all([signalData is None for _, signalData in signals]):
        return None, None

    images = common.mapList(
        zip(leads, signals),
        lambda leadSignalPair: (
            leadSignalPair[1][0],
            visualization.overlaySignalOnImage(leadSignalPair[1][1],
            leadSignalPair[0][1].roiData.pixelData)
        )
    )

    # Map leads to grid size estimates
    gridSpacings = common.mapList(leads, lambda pair: (pair[0], (extractGrid(pair[1].roiData.pixelData))))
    horizontalSpacings = [hSpace for _, (hSpace, _) in gridSpacings if hSpace is not None]
    verticalSpacings   = [vSpace for _, (_, vSpace) in gridSpacings if vSpace is not None]

    if len(horizontalSpacings) == 0 or len(verticalSpacings) == 0:
        return None, None

    samplingPeriodInPixels = common.mean(horizontalSpacings)
    gridHeightInPixels = common.mean(verticalSpacings)

    # Scale signals
    # TODO: Pass in the grid size in mm
    signals = common.mapList(signals, lambda pair: (pair[0], signal.verticallyScaleECGSignal(signal.zeroECGSignal(pair[1]), gridHeightInPixels, ecgData.gridVoltageScale, gridSizeInMillimeters=1.0)))

    # TODO: Pass in the grid size in mm
    samplingPeriod = signal.ecgSignalSamplingPeriod(samplingPeriodInPixels, ecgData.gridTimeScale, gridSizeInMillimeters=1.0)

    # 3. Zero pad all signals on the left based on their start times and the samplingPeriod
    # take the max([len(x) for x in signals]) and zero pad all signals on the right
    paddedSignals = [(key, common.padLeft(signal, int(leadData.leadStartTime / samplingPeriod))) for (key, signal), (_, leadData) in zip(signals, leads)]

    # (should already be handled by (3)) Replace any None signals with all zeros
    length = max([len(s) for _, s in paddedSignals])
    fullSignals = [(key, common.padRight(signal, length - len(signal))) for (key, signal) in paddedSignals]

    return dict(fullSignals), dict(images)


def exportSignals(leadSignals, filePath, separator='\t'):
    """Exports a dict of lead signals to file

    Args:
        leadSignals (Dict[str -> np.ndarray]): Dict mapping lead id's to np array of signal data (output from convertECGLeads)
    """
    leads = common.zipDict(leadSignals)
    leads.sort(key=lambda pair: LEAD_ORDER[pair[0]])

    assert len(leads) >= 1
    lengthOfFirst = len(leads[0][1])

    assert all([len(signal) == lengthOfFirst for key, signal in leads])

    collated = np.array([signal for key, signal in leads])
    output = np.swapaxes(collated, 0, 1)

    if not issubclass(type(filePath), Path):
        filePath = Path(filePath)

    if filePath.exists():
        print("Warning: Output file will be overwritten!")

    outputLines = [
        separator.join(
            [str(val) for val in row]
        ) + "\n"
        for row in output
    ]

    with open(filePath, 'w') as outputFile:
        outputFile.writelines(outputLines)
