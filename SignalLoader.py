import numpy as np

from Utility import *

# Not using rn, but maybe this is useful?
class SignalData:
    I = None
    II = None
    III = None
    aVR = None
    aVL = None
    aVF = None

    V1 = None
    V2 = None
    V4 = None
    V3 = None
    V5 = None
    V6 = None


def leadValues(text: str, conversion) -> bool:
    if '\t' in text:
        words = text.split('\t')
    elif ',' in text:
        words = text.split(',')
    else:
        words = text.split(' ')

    areFloats = list(map(isFloat, words))

    if not allTrue(areFloats):
        print("Not all floats!:", words)
        return None

    values = list(map(conversion, words))
    return values


def load(fileName: str) -> SignalData:
    values = []

    with open(fileName, 'r') as file:
        for line in file.readlines():
            text = line.strip()
            valuesAtTime = leadValues(text, float) # ⚠️ Should this ever be float?

            if valuesAtTime is not None:
                values.append(valuesAtTime)

    leads = np.swapaxes(np.array(values),0,1)

    print("Loaded leads:", leads.shape)

    return leads
