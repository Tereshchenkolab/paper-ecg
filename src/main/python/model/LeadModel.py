    """This class models individual leads, including its ID, start time, its ROI on
    the image.
    """
class Lead:
    def __init__(self, leadId, roiData, leadStartTime=0.0):
        self.leadId = leadId
        self.roiData = roiData
        self.leadStartTime = leadStartTime
