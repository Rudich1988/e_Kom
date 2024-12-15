from fastapi import FastAPI

from src.project.db.mongo_db import init_db

app = FastAPI()

init_db()


from src.project.form_templates.routers import router as forms_router


app.include_router(forms_router)
