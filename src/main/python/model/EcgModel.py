from views.ImageView import *

class EcgModel:
    def __init__(self):
        self.leads = {}
        self.gridVoltageScale = 0.0
        self.gridTimeScale = 0.0

    def printLeadInfo(self):
        for lead in self.leads.items():
            print(lead)
