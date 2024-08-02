from mongomock.mongo_client import MongoClient

class InMemoryDatabase:
    _instance = None

    def __new__(cls) -> MongoClient:
        if cls._instance is None:
            client = MongoClient()
            cls._instance = client.get_database('memory_db')
        return cls._instance
    
    @staticmethod
    def connection_test():
        try:
            db = InMemoryDatabase()
            collections = db.list_collection_names()
            return collections is not None
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False