from dataclasses import fields
from http import HTTPStatus

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from src.project.form_templates.dto.forms_dto import FormTemplateDto
from src.project.form_templates.repositories.mongo_db_repository import (
    FormTemplateRepository
)
from src.project.form_templates.schemas.forms_schemas import (
    FormTemplateSchema
)
from src.project.form_templates.services.forms_service import FormService
from src.project.fields.schemas.fields_schemas import FieldsSchema
from src.project.fields.dto.fields_dto import FieldsDTO

router = APIRouter(
    prefix='',
    tags=['Forms']
)


@router.post(
    '/get_form',
    response_model=FormTemplateSchema
)
async def get_form(
        fields_data: FieldsSchema = Body(...)
):
    #try:

    form_data = FieldsDTO(
        fields=fields_data.root
    )
    form_template_data = await FormService(
        repository=FormTemplateRepository(
            collection_name='form_templates'
        )
    ).get_suitable_form_template(
        data=form_data
    )
    if isinstance(form_template_data, FormTemplateDto):
        FormTemplateSchema(
            id=form_template_data.id,
            name=form_template_data.name,
            fields=form_template_data.fields
        )
        return JSONResponse(
            content={
                "form name": form_template_data.name
            },
            status_code=HTTPStatus.OK
        )
    fields = FieldsSchema(
        fields=form_template_data.fields
    )
    return JSONResponse(
        content=fields.fields,
        status_code=HTTPStatus.NOT_FOUND
    )
    #except