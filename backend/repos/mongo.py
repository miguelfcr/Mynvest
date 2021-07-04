from pymongo import MongoClient

DNS_PADRAO = 'mongodb+srv://mynvest:mynvest@cluster0.6dv4w.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

class MongoRepo:
    def __init__(self, dns=DNS_PADRAO, base="mynvest", collection="acoes"):
        client = MongoClient(DNS_PADRAO)
        self.db = client[base]
        self.collection = self.db[collection]

    def insert(self, row):
        row_id = self.collection.insert_one(row).inserted_id
        return row_id

    def select(self, query_dict, limit=999999):
        row_list = self.collection.find(query_dict).limit(limit)
        return row_list

    def select_one(self, query_dict):
        row_dict = self.collection.find_one(query_dict)
        return row_dict

    def update_one(self, where_dict, update_dict):
        modified_count = self.collection.update_one(where_dict, {'$set': update_dict}).modified_count
        return modified_count

    def delete_one(self, where_dict):
        deleted_count = self.collection.delete_one(where_dict).deleted_count
        return deleted_count
    
    def update_insert(self, where_dict, update_dict):
        row_id = self.collection.update(where_dict, update_dict, upsert=True)
        return row_id