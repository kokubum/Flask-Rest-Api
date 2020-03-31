from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        return {'message': 'Store not found'},404 #tuple(message to the body and 404 to the status code)
    
    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message': f'The store {name} already exist'},404

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message':'An error ocurred'} ,500
        
        return store.json(),201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store was deleted'}
        

class StoreList(Resource):
    def get(self):
        return {'Stores': [store.json() for store in StoreModel.query.all()]}