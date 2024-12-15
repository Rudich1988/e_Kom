from typing import Literal

from pydantic import BaseModel, RootModel

from src.project.enums.types_enums import Types


class FieldsSchema(RootModel):
    root: dict[str, str]

    class Config:
        json_schema_extra = {
            "example": {
                "field_name": "any text",
                "email": "exmple@mail.ru",
                "date": "11.12.1995",
                "date_2": "1995-11.12",
                "phone": "+79261234567"
            }
        }


class FieldSchema(BaseModel):
    name: str
    type: Literal[
        Types.TEXT,
        Types.EMAIL,
        Types.DATE,
        Types.PHONE
    ]
