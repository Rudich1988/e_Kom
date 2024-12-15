from dataclasses import fields
from datetime import datetime
from typing import Optional
import re

from email_validator import (
    validate_email,
    EmailNotValidError
)

from src.project.enums.types_enums import Types
from src.project.fields.dto.fields_dto import FieldsDTO, ValidatedFieldsDTO, FieldDTO


class FieldsConverterService:
    def set_date_type(
            self,
            value: str
    ) -> Optional[str]:
        for date_format in [
            '%d.%m.%Y', '%Y-%m-%d'
        ]:
            try:
                datetime.strptime(
                    value,
                    date_format
                )
                return Types.DATE
            except ValueError:
                continue

    def set_phone_type(
            self,
            value: str
    ) -> Optional[str]:
        phone_cleaned = re.sub(
            r'[^0-9+]',
            '',
            value
        )
        if (phone_cleaned.startswith("+7")
                and len(phone_cleaned) == 12
                and phone_cleaned[2:].isdigit()
        ):
            return Types.PHONE

    def set_email_type(
            self,
            value: str
    ) -> Optional[str]:
        try:
            validate_email(value)
            return Types.EMAIL
        except EmailNotValidError:
            pass

    def set_value_type(
            self,
            value: str
    ) -> str:
        if self.set_date_type(
            value
        ):
            return Types.DATE
        if self.set_phone_type(
            value
        ):
            return Types.PHONE
        if self.set_email_type(
            value
        ):
            return Types.EMAIL
        return Types.TEXT

    def set_types_fields(
            self,
            data: FieldsDTO
    ) -> ValidatedFieldsDTO:
        validated_fields = [
            FieldDTO(
             name=field_name,
             type=self.set_value_type(
                 field_value
             )
            )
            for field_name,
            field_value in data.fields.items()
        ]
        '''
            {
            field: self.set_value_type(value)
            for field, value
            in data.fields.items()
        }
        return FieldsDTO(
            fields=fields
        )
        '''
        return ValidatedFieldsDTO(
            validated_fields=validated_fields
        )
