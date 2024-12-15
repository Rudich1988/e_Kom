from typing import Union

from fastapi import HTTPException, status

from src.project.core.mongodb_repository import MongoDBRepository
from src.project.fields.dto.fields_dto import FieldsDTO, FieldDTO, ValidatedFieldsDTO
from src.project.form_templates.dto.forms_dto import FormTemplateDto


class FormTemplateRepository(
    MongoDBRepository
):
    def create_form_template_dto(
            self,
            form
    ) -> FormTemplateDto:
        fields = [
            FieldDTO(
                name=field.name,
                type=field.type
            ) for field in form.fields
        ]
        form_template = FormTemplateDto(
            id=form.id,
            name=form.name,
            fields=fields
        )
        return form_template

    async def get(
            self,
            data: dict
    ) -> FormTemplateDto:
        ...

    async def get_suitable_form_template(
            self,
            data: ValidatedFieldsDTO
    ) -> Union[FormTemplateDto, None]:
        form = list(self.collection.aggregate([
            {
                "$match": {
                    "$expr": {
                        "$lte": [
                            {"$size": "$fields"},
                            len(data.validated_fields)
                        ]
                        # len(fields) <= len(validated_list)
                    }
                }
            },
            {
                # Подсчитываем количество совпадений для каждого шаблона
                "$project": {
                    "_id": 1,
                    "name": 1,  # Имя шаблона
                    "fields": 1,  # Поля шаблона
                    "matching_fields_count": {
                        "$size": {
                            "$filter": {
                                "input": "$fields",  # Поля из шаблона
                                "as": "template_field",  # Ссылка на каждый элемент шаблона
                                "cond": {
                                    "$and": [
                                        # Проверяем, что значение name совпадает с name в validated_list
                                        {
                                            "$in": [
                                                "$$template_field.name",
                                                [
                                                 field.name
                                                 for field
                                                 in data.validated_fields
                                                ]
                                            ]
                                        },
                                        # Проверяем, что значение type совпадает с type в validated_list
                                        {
                                            "$in": [
                                                "$$template_field.type",
                                                [
                                                 field.type
                                                 for field
                                                 in data.validated_fields]
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            {
                # Сортируем шаблоны по количеству совпадений (по убыванию)
                "$sort": {
                    "matching_fields_count": -1
                }
            },
            {
                # Ограничиваем результат одним шаблоном с максимальными совпадениями
                "$limit": 1
            }
        ]))
        if form:
            return self.create_form_template_dto(
                form=form[0]
            )
