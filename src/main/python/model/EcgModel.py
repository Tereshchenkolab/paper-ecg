from views.ImageView import *

class EcgModel:
    def __init__(self):
        super().__init__()
        self.leads = [None]*12
        self.gridVoltageScale = None
        self.gridTimeScale = None

