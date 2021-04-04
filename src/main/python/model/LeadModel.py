from enum import Enum

class LeadIdEnum(Enum):
    I = 0
    II = 1
    III = 2
    aVR = 3
    aVL = 4
    aVF = 5
    V1 = 6
    V2 = 7
    V3 = 8
    V4 = 9
    V5 = 10
    V6 = 11

class Lead:
    def __init__(self, leadId, roiData, leadStartTime=None):
        super().__init__()
        self.leadId = leadId
        self.roiData = roiData
        self.leadStartTime = leadStartTime