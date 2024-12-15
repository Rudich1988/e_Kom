from http import HTTPStatus

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from pydantic_core._pydantic_core import ValidationError

from src.project.form_templates.dto.forms_dto import FormTemplateDto
from src.project.form_templates.repositories.mongo_db_repository import (
    FormTemplateRepository
)
from src.project.form_templates.schemas.forms_schemas import (
    FormNameSchema
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
    response_model=FormNameSchema
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
    if isinstance(
            form_template_data,
            FormTemplateDto
    ):
        form_name = FormNameSchema(
            name=form_template_data.name
        )
        return JSONResponse(
            content=form_name.model_dump(),
            status_code=HTTPStatus.OK
        )
    fields = FieldsSchema(
        root=form_template_data.fields
    )
    return JSONResponse(
        content=fields.root,
        status_code=HTTPStatus.NOT_FOUND
    )
    '''
    except ValidationError:
        return JSONResponse(
            content={
                "error": "incorrect request data"
            },
            status_code=HTTPStatus.BAD_REQUEST
        )
    except Exception:
        return JSONResponse(
            content={
                "error": "server error"
            }
        )
    '''
