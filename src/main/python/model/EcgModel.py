"""This class models the full ECG, includeing its leads and grid scales
"""
class Ecg:

    DEFAULT_TIME_SCALE = 25
    DEFAULT_VOLTAGE_SCALE = 10

    def __init__(self):
        self.leads = {}
        self.gridVoltageScale = Ecg.DEFAULT_VOLTAGE_SCALE
        self.gridTimeScale = Ecg.DEFAULT_TIME_SCALE

    def printLeadInfo(self):
        for lead in self.leads.items():
            print(lead)
