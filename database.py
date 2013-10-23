from pymongo import MongoClient

# Conectaser a la base de datos, guardar, editar y eliminar datos, 
# Realizar queries

class db:
    client = MongoClient()
    
    def __init__(self,db):
        self.db = self.client[db]
        
    def insert(self,post):
        post_id = self.db.insert(post)
        return post_id