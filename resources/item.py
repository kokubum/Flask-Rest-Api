import sqlite3
from flask_restful import reqparse,Resource
from flask_jwt import jwt_required
from models.item import ItemModel


#Using flask-restful we don't need to do jsonify, we only return dictionarys, and the library do that for us
class Item(Resource):
    #Parser will belong to the class itself, and not one specific object
    parse = reqparse.RequestParser()
    parse.add_argument('price',type=float,required=True,help='this field cannot be blank')
    parse.add_argument('store_id',type=int,required=True,help='this field cannot be blank')


    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() 
        return {'message':'Item not found'},400

    def post(self,name):
        
        if ItemModel.find_by_name(name):
            return {'message': 'Item already exist'}
       
        data = Item.parse.parse_args()
        item = ItemModel(name,**data) 

        try:
            item.save_to_db()
        except:
            return {'message':'An error ocurred inserting the item'},500 #internal server error

        return item.json(),201

    

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':'Item deleted'}


    def put(self,name):
        #data = request.get_json()
        data = Item.parse.parse_args()       #will receive the JSON, and accept only the choosing field to put in data
        
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name,**data)
        else:
            item.price = data['price']
        item.save_to_db()     
        return item.json()

    
class ItemList(Resource):
    def get(self):
        return {'Item':[item.json() for item in ItemModel.query.all()]}
        #or return {'Item': list(map(lambda x: x.json,ItemModel.query.all()))}
    