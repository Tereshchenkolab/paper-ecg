"""
lead.py

Type representing an ECG lead.
"""

from enum import Enum
import dataclasses


class LeadId(Enum):
    """Enumerates the different names for leads

    `Enum` provides lots of awesome functionality:

      - Check if a string is a valid member of this enum:
        ```
        someString in Lead.__members__
        ```

      - Convert a string to enum:
        ```
        myLead = Lead[someString]
        ```
    """

    I   = 0
    II  = 1
    III = 2
    aVR = 3
    aVL = 4
    aVF = 5
    V1  = 6
    V2  = 7
    V3  = 8
    V4  = 9
    V5  = 10
    V6  = 11

    def __repr__(self) -> str:
        names = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        return names[self.value]


@dataclasses.dataclass(frozen=True)
class Lead:
    x: int
    y: int
    width: int
    height: int
    startTime: int

