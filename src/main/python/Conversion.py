from pathlib import Path

import numpy as np

from model.EcgModel import Ecg
from ECGToolkit.Common import *
from ECGToolkit.Process import extractSignalFromImage, extractGridFromImage, ecgSignalSamplingPeriod, verticallyScaleECGSignal, zeroECGSignal
from ECGToolkit import SignalDetection
from ECGToolkit import SignalExtraction
from ECGToolkit import GridDetection
from ECGToolkit.Visualization import overlaySignalOnImage


LEAD_ORDER = {
    leadID: i for i, leadID
    in enumerate(["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"])
}


def convertECGLeads(ecgData: Ecg):

    # TODO: Make parameters
    signalDetectionMethod = partial(SignalDetection.mallawaarachchi, useBlur=True)
    signalExtractionMethod = SignalExtraction.naïveHorizontalScan

    gridDetectionMethod = GridDetection.kernelApproach

    leads = zipDict(ecgData.leads)

    extractSignal = partial(extractSignalFromImage, detectionMethod=signalDetectionMethod, extractionMethod=signalExtractionMethod)
    extractGrid   = partial(extractGridFromImage, detectionMethod=gridDetectionMethod)

    # Map all lead images to signal data
    signals = mapList(leads, lambda pair: (pair[0], extractSignal(pair[1].roiData.pixelData)))

    # If all signals failed -> Failure
    if all([signalData is None for _, signalData in signals]):
        return None

    images = mapList(
        zip(leads, signals),
        lambda leadSignalPair: (leadSignalPair[1][0], overlaySignalOnImage(leadSignalPair[1][1], leadSignalPair[0][1].roiData.pixelData))
    )

    # Map leads to grid size estimates
    gridSpacings = mapList(leads, lambda pair: (pair[0], (extractGrid(pair[1].roiData.pixelData))))
    horizontalSpacings = [hSpace for _, (hSpace, _) in gridSpacings if hSpace is not None]
    verticalSpacings   = [vSpace for _, (_, vSpace) in gridSpacings if vSpace is not None]

    if len(horizontalSpacings) == 0 or len(verticalSpacings) == 0:
        return None

    samplingPeriodInPixels = mean(horizontalSpacings)
    gridHeightInPixels = mean(verticalSpacings)

    # Scale signals
    # TODO: Pass in the grid size in mm
    signals = mapList(signals, lambda pair: (pair[0], verticallyScaleECGSignal(zeroECGSignal(pair[1]), gridHeightInPixels, ecgData.gridVoltageScale, gridSizeInMillimeters=1.0)))

    # TODO: Pass in the grid size in mm
    samplingPeriod = ecgSignalSamplingPeriod(samplingPeriodInPixels, ecgData.gridTimeScale, gridSizeInMillimeters=1.0)

    # 3. Zero pad all signals on the left based on their start times and the samplingPeriod
    # take the max([len(x) for x in signals]) and zero pad all signals on the right
    paddedSignals = [(key, padLeft(signal, int(leadData.leadStartTime / samplingPeriod))) for (key, signal), (_, leadData) in zip(signals, leads)]

    # (should already be handled by (3)) Replace any None signals with all zeros
    length = max([len(s) for _, s in paddedSignals])
    fullSignals = [(key, padRight(signal, length - len(signal))) for (key, signal) in paddedSignals]

    return dict(fullSignals), dict(images)


def exportSignals(leadSignals, filePath, separator='\t'):
    """Exports a dict of lead signals to file

    Args:
        leadSignals (Dict[str -> np.ndarray]): Dict mapping lead id's to np array of signal data (output from convertECGLeads)
    """
    leads = zipDict(leadSignals)
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
