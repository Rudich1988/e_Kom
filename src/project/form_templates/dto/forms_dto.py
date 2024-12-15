from dataclasses import dataclass

from bson import ObjectId

from src.project.fields.dto.fields_dto import FieldDTO


@dataclass
class FormTemplateDto:
    id: ObjectId
    name: str
    fields: list[FieldDTO]
