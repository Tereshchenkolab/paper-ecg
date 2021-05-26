"""
lead.py

Type representing an ECG lead.
"""

from enum import Enum


class Lead(Enum):
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

    I = 'I'
    II = 'II'
    III = 'III'

    aVR = 'aVR'
    aVL = 'aVL'
    aVF = 'aVF'

    V1 = 'V1'
    V2 = 'V2'
    V3 = 'V3'

    V4 = 'V4'
    V5 = 'V5'
    V6 = 'V6'

    A1 = 'A1'
    A2 = 'A2'
    A3 = 'A3'
