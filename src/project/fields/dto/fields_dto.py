from dataclasses import dataclass, field

from typing import Literal

from src.project.enums.types_enums import Types


@dataclass
class FieldsDTO:
    fields: dict[str, str] = field(
        default_factory=dict
    )


@dataclass
class FieldDTO:
    name: str
    type: Literal[
        Types.DATE,
        Types.TEXT,
        Types.EMAIL,
        Types.PHONE
    ]


@dataclass
class ValidatedFieldsDTO:
    validated_fields: list[FieldDTO]


@dataclass
class FieldsDTO:
    fields: dict[str, str] = field(
        default_factory=dict
    )
