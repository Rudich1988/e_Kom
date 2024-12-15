from typing import Union

from src.project.fields.dto.fields_dto import FieldsDTO
from src.project.form_templates.dto.forms_dto import FormTemplateDto
from src.project.form_templates.repositories.mongo_db_repository import (
    FormTemplateRepository
)
from src.project.fields.services.fields_converter_service import (
    FieldsConverterService
)


class FormService:
    def __init__(
            self,
            repository: FormTemplateRepository
    ) -> None:
        self.repository = repository

    async def get(self, data: str):
        ...

    async def get_suitable_form_template(
            self,
            data: FieldsDTO
    ) -> Union[
        FormTemplateDto,
        FieldsDTO
    ]:
        validated_fields = (
            FieldsConverterService().
            set_types_fields(data=data)
        )
        form_data = (
            await self.repository.
            get_suitable_form_template(
                data=validated_fields
            )
        )
        if form_data:
            return form_data
        return FieldsDTO(
            fields = {
                field.name: field.type.value
                for field in validated_fields.
                validated_fields
            }
        )
