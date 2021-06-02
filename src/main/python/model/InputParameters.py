from typing import Dict
import dataclasses

from model.Lead import LeadId, Lead


@dataclasses.dataclass(frozen=True)
class InputParameters:
    rotation: int
    timeScale: int
    voltScale: int
    leads: Dict[LeadId, Lead]
