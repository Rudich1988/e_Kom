from pymongo import MongoClient, ASCENDING
from pymongo.errors import OperationFailure

from src.project.config.base import Config

MONGO_URI = Config.MONGO_URI
client = MongoClient(MONGO_URI)
db = client.get_database()


def init_db():
    try:
        collection = db["form_templates"]
        if collection.find_one({}) is None:
            collection.create_index(
                [("name", ASCENDING)],
                unique=True
            )
            collection.create_index(
                [("fields.name", ASCENDING)],
                name="field_name_index"
            )
            collection.create_index(
                [("fields.type", ASCENDING)],
                name="field_type_index"
            )

            print(
                "MongoDB connected and "
                "indexes created successfully."
            )

            collection.insert_many([
                {
                    "name": "Product Form",
                    "fields": [
                        {"product": "apple", "type": "text"},
                        {"name": "delivery_date", "type": "date"}
                    ]
                },
                {
                    "name": "User Form",
                    "fields": [
                        {"name": "first_name", "type": "text"},
                        {"name": "email", "type": "email"}
                    ]
                },
                {
                    "name": "Customer Form",
                    "fields": [
                        {"name": "first_name", "type": "text"},
                        {"name": "email", "type": "email"},
                        {"name": "phone_number", "type": "phone"},
                        {"name": "last_vizit", "type": "date"}
                    ]
                }
            ])
    except ConnectionError as e:
        print("Ошибка подключения к MongoDB:", e)
    except OperationFailure as e:
        print("Ошибка при операции с коллекцией:", e)
    except Exception as e:
        print("Произошла непредвиденная ошибка:", e)
