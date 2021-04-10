from enum import Enum

class Lead:
    def __init__(self, leadId, roiData, leadStartTime=0.0):
        self.leadId = leadId
        self.roiData = roiData
        self.leadStartTime = leadStartTime

        