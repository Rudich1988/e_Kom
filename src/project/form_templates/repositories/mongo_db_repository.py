from typing import Union

from src.project.core.mongodb_repository import MongoDBRepository
from src.project.fields.dto.fields_dto import FieldDTO, ValidatedFieldsDTO
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
                name=field['name'],
                type=field['type']
            ) for field in form['fields']
        ]
        form_template = FormTemplateDto(
            id=form['_id'],
            name=form['name'],
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
        form = list(
            self.collection.aggregate([
                {
                    "$match": {
                        "$expr": {
                            "$lte": [
                                {"$size": "$fields"},
                                len(data.validated_fields)
                            ]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "name": 1,
                        "fields": 1,
                        "matching_fields_count": {
                            "$size": {
                                "$filter": {
                                    "input": "$fields",
                                    "as": "template_field",
                                    "cond": {
                                        "$and": [
                                            {
                                                "$in": [
                                                    "$$template_field.name",
                                                    [
                                                        field.name
                                                        for field in
                                                        data.validated_fields
                                                    ]
                                                ]
                                            },
                                            {
                                                "$in": [
                                                    "$$template_field.type",
                                                    [
                                                        field.type.value
                                                        for field in
                                                        data.validated_fields
                                                    ]
                                                ]
                                            }
                                        ]
                                    }
                                }
                            }
                        },
                        "fields_count": {"$size": "$fields"}
                    }
                },
                {
                    "$match": {
                        "$expr": {
                            "$eq": [
                                "$matching_fields_count", "$fields_count"
                            ]
                        }
                    }
                },
                {
                    "$sort": {
                        "matching_fields_count": -1
                    }
                },
                {
                    "$limit": 1
                }
            ])
        )
        if form:
            return self.create_form_template_dto(
                form=form[0]
            )
