from bson import ObjectId
from pydantic import BaseModel, field_validator

from src.project.fields.schemas.fields_schemas import FieldSchema


class FormTemplateSchema(BaseModel):
    id: str
    name: str
    fields: list[FieldSchema]

    @field_validator('id', mode='before')
    def objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        json_encoders = {
            ObjectId: str
        }

class FormNameSchema(BaseModel):
    name: str
