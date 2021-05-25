"""
metadata.py

Contains classes and functions for handling metadata associated with leads used as inputs to
the extraction process. "Metadata" generally refers to non-image, human-provided data.
"""
import json
from typing import Any, Dict, List, Optional, Union
import dataclasses
import pathlib

from . import lead


@dataclasses.dataclass(frozen=True)
class CropLocation():
    x: int
    y: int
    width: int
    height: int

    def toDict(self):
        return {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
        }

    @classmethod
    def fromDict(cls, dictionary: Dict[str, int]):
        assert ('x' in dictionary and 'y' in dictionary and 'width' in dictionary and 'height' in dictionary), \
            "`CropLocation.fromDict` requires keys ['x', 'y', 'weight', 'height']."

        return cls(
            x=dictionary['x'],
            y=dictionary['y'],
            width=dictionary['width'],
            height=dictionary['height'],
        )


@dataclasses.dataclass(frozen=True)
class LeadMetadata():
    file: pathlib.Path  # This is guaranteed to be a file on disk
    timeScale: float
    voltageScale: float
    cropping: Optional[CropLocation] = None
    start: Optional[Union[float, int]] = 0

    def __post_init__(self):
        assert self.file.exists()

    @staticmethod
    def outputFilePath(filePath: pathlib.Path) -> str:
        return str(filePath.absolute())

    def toDict(self):
        dictionary = {'file': LeadMetadata.outputFilePath(self.file), 'timeScale': self.timeScale, 'voltageScale': self.voltageScale}
        if self.start != 0:
            dictionary['start'] = self.start
        if self.cropping is not None:
            dictionary['cropping'] = self.cropping.toDict()
        return dictionary

    @classmethod
    def fromDict(cls, dictionary: Dict[str, Any]):
        assert ('file' in dictionary and 'timeScale' in dictionary and 'voltageScale' in dictionary), \
            "`LeadMetadata.fromDict` requires keys ['file', 'timeScale', 'voltageScale']."

        return cls(
            file=dictionary.pop('file'),
            timeScale=dictionary.pop('timeScale'),
            voltageScale=dictionary.pop('voltageScale'),
            cropping=CropLocation.fromDict(dictionary.pop('cropping')) if 'cropping' in dictionary else None,
            start=dictionary.pop('start', 0),
        )


EcgMetadata = Dict[lead.Lead, LeadMetadata]


def valueOfAll(items: List[Any]) -> Optional[Any]:
    assert len(items) > 0

    first = items[0]
    if all(first == item for item in items[1:]):
        return first
    else:
        return None


def serializeEcgMetdata(data: EcgMetadata) -> str:
    sharedFile: Optional[str] = valueOfAll([LeadMetadata.outputFilePath(meta.file) for _, meta in data.items()])
    sharedTimeScale: Optional[int] = valueOfAll([meta.timeScale for _, meta in data.items()])
    sharedVoltageScale: Optional[int] = valueOfAll([meta.voltageScale for _, meta in data.items()])

    def convertLead(leadMetadata: LeadMetadata) -> Dict[str, Any]:
        dictionary = leadMetadata.toDict()
        # Delete any metadata that are the same for all leads to save file space
        if sharedFile is not None:
            dictionary.pop('file')
        if sharedTimeScale is not None:
            dictionary.pop('timeScale')
        if sharedVoltageScale is not None:
            dictionary.pop('voltageScale')
        return dictionary

    outputDictionary: Dict[str, Any] = {lead.value: convertLead(meta) for lead, meta in data.items()}

    # Add any metadata that are the same for all leads
    if sharedFile is not None:
        outputDictionary['file'] = sharedFile
    if sharedTimeScale is not None:
        outputDictionary['timeScale'] = str(sharedTimeScale)
    if sharedVoltageScale is not None:
        outputDictionary['voltageScale'] = str(sharedVoltageScale)

    return json.dumps(outputDictionary)


def deserializeEcgMetdata(jsonSerial: str) -> EcgMetadata:
    inputDictionary = json.loads(jsonSerial)

    sharedFile: Optional[str] = inputDictionary.pop('file') if 'file' in inputDictionary else None
    sharedTimeScale: Optional[int] = inputDictionary.pop('timeScale') if 'timeScale' in inputDictionary else None
    sharedVoltageScale: Optional[int] = inputDictionary.pop('voltageScale') if 'voltageScale' in inputDictionary else None

    def parseLead(dictionary: Dict[str, Any]) -> LeadMetadata:
        # Delete any metadata that are the same for all leads to save file space
        if sharedFile is not None:
            dictionary['file'] = pathlib.Path(sharedFile)
        if sharedTimeScale is not None:
            dictionary['timeScale'] = sharedTimeScale
        if sharedVoltageScale is not None:
            dictionary['voltageScale'] = sharedVoltageScale

        return LeadMetadata.fromDict(dictionary)

    ecgMetadata = {lead.Lead[leadName]: parseLead(data) for leadName, data in inputDictionary.items() if leadName in lead.Lead.__members__}

    return ecgMetadata


def writeEcgMetadata(data: EcgMetadata, filePath: pathlib.Path):
    assert isinstance(filePath, pathlib.Path)
    assert not filePath.is_dir()
    # TODO: Error handle the path

    jsonSerial = serializeEcgMetdata(data)

    with filePath.open('w') as file:
        file.write(jsonSerial)


def loadEcgMetadata(filePath: pathlib.Path) -> EcgMetadata:
    assert isinstance(filePath, pathlib.Path)
    assert filePath.exists()
    # TODO: Error handle the path

    jsonSerial = None

    with filePath.open() as file:
        jsonSerial = file.read()

    assert jsonSerial is not None, "Unable to load JSON!"

    return deserializeEcgMetdata(jsonSerial)
