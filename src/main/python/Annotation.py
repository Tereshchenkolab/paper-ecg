"""
metadata.py

Contains classes and functions for handling metadata associated with leads used as inputs to
the extraction process. "Metadata" generally refers to non-image, human-provided data.
"""
from os import path
import dataclasses
import json
import pathlib
import datetime
from typing import Any, Dict, List, Optional, Union

from model import Lead


VERSION = 0


def noneValuesRemoved(dictionary: Dict[Any, Any]) -> Dict[Any, Any]:
    return {key: value for key, value in dictionary.items() if value is not None}


@dataclasses.dataclass(frozen=True)
class CropLocation():
    x: int
    y: int
    width: int
    height: int

    def __post_init__(self):
        assert isinstance(self.x, int)
        assert isinstance(self.y, int)
        assert isinstance(self.width, int)
        assert isinstance(self.height, int)


@dataclasses.dataclass(frozen=True)
class ImageMetadata():
    name: str
    directory: Optional[str] = None
    hashValue: Optional[Any] = None


@dataclasses.dataclass(frozen=True)
class LeadAnnotation:
    cropping: CropLocation
    start: Union[float, int]


@dataclasses.dataclass(frozen=True)
class Schema:
    name: str
    version: int

    def __post_init__(self):
        assert isinstance(self.name, str)
        assert '.' not in self.name
        assert isinstance(self.version, int)

    def __repr__(self) -> str:
        return f"{self.name}.{self.version}"


@dataclasses.dataclass(frozen=True)
class Annotation:
    """Stores annotations made by the user to save their work for later.

    Example:
    ```
    Annotation(
        ImageMetadata("fullscan.png"), # Optionally, directory and hashValue
        0.0,  # Rotation
        25.0,  # Time scale
        10.0,  # Voltage Scale
        {
            Lead.LeadName.I: LeadAnnotation(
                CropLocation(0, 0, 20, 40),
                0.0
            ),
            Lead.LeadName.III: LeadAnnotation(
                CropLocation(0, 0, 20, 40),
                0.0
            )
        }
    )
    ```
    """
    schema: Schema = dataclasses.field(
        default=Schema("paper-ecg-user-annotation", VERSION), init=False
    )

    timeStamp: str
    image: ImageMetadata
    rotation: Union[int, float]
    timeScale: Union[int, float]
    voltageScale: Union[int, float]
    leads: Dict[Lead.LeadId, LeadAnnotation]

    def toDict(self):
        dictionary = dataclasses.asdict(self)  # <3 dataclasses

        # Need to customize the leads to convert enum to string
        dictionary["leads"] = {
            lead.name: dataclasses.asdict(annotation) for lead, annotation in self.leads.items()
        }
        # Remove None entries from the image since it has optional fields
        dictionary["image"] = noneValuesRemoved(dataclasses.asdict(self.image))

        return dictionary

    def save(self, filePath: pathlib.Path):
        dictionary = self.toDict()
        jsonSerial = json.dumps(dictionary)

        with filePath.open('w') as file:
            file.write(jsonSerial)
