from views.ImageView import *

class EcgModel:
    def __init__(self):
        self.leads = [None]*12
        self.gridVoltageScale = 0.0
        self.gridTimeScale = 0.0

    def printLeadInfo(self):
        for lead in self.leads:
            if lead is not None:
                print("Lead Id: " + lead.leadId.name)
                print("Start Time: " + str(lead.leadStartTime))
