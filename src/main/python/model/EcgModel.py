"""This class models the full ECG, includeing its leads and grid scales
"""
class Ecg:
    def __init__(self):
        self.leads = {}
        self.gridVoltageScale = 1.0
        self.gridTimeScale = 1.0

    def printLeadInfo(self):
        for lead in self.leads.items():
            print(lead)
