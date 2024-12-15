from src.project.core.abstract_repository import AbstractRepository
from src.project.db.mongo_db import db



class MongoDBRepository(AbstractRepository):
    def __init__(
            self,
            collection_name: str
    ) -> None:
        self.collection = db[
            collection_name
        ]

    async def get(self, data):
        raise NotImplementedError
