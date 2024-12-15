from pymongo import MongoClient, ASCENDING
from pymongo.errors import OperationFailure

from src.project.config.base import Config

#MONGO_URI = Config.MONGO_URI
#client = MongoClient(MONGO_URI)
#db = client.get_database()

#def get_db():
 #   return db

def init_db():
    '''
    collection = db["form_templates"]

    # Создаем индексы
    collection.create_index([("name", ASCENDING)], unique=True)
    collection.create_index([("fields.name", ASCENDING)], name="field_name_index")
    collection.create_index([("fields.type", ASCENDING)], name="field_type_index")
    print("MongoDB connected and indexes created.")


    # Если коллекция пустая, можно добавить данные по умолчанию (если нужно)
    if collection.count_documents({}) == 0:
        # Добавить несколько шаблонов для примера
        collection.insert_many([
            {
                "name": "Product Form",
                "fields": [{"product": "apple", "type": "text"}, {"name": "delivery_date", "type": "date"}]
            },
            {
                "name": "User Form",
                "fields": [{"name": "first_name", "type": "text"}, {"name": "email", "type": "email"}]
            }
        ])
    else:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    #print("Database initialized.")
    '''
    try:
        client = MongoClient(Config.MONGO_URI)
        db = client.get_database()  # Получаем базу данных

        # Проверка соединения с базой данных
        client.admin.command('ping')  # Пинг для проверки, что сервер доступен

        collection = db["form_templates"]

        # Создаем индексы
        collection.create_index([("name", ASCENDING)], unique=True)
        collection.create_index([("fields.name", ASCENDING)], name="field_name_index")
        collection.create_index([("fields.type", ASCENDING)], name="field_type_index")

        print("MongoDB connected and indexes created successfully.")

    except ConnectionError as e:
        print("Ошибка подключения к MongoDB:", e)
    except OperationFailure as e:
        print("Ошибка при операции с коллекцией:", e)
    except Exception as e:
        print("Произошла непредвиденная ошибка:", e)
