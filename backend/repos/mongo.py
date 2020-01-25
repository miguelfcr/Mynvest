from pymongo import MongoClient

DNS_PADRAO = 'mongodb+srv://mongodb:mongoDB@cluster0-vvgvw.mongodb.net/test?retryWrites=true&w=majority'

class MongoRepo:
    def __init__(self, dns=DNS_PADRAO, base="mynvest", collection="fundamentus"):
        client = MongoClient(dns)
        self.db = client[base]
        self.collection = self.db[collection]

    def insert(self, row):
        row_id = self.collection.insert_one(row).inserted_id
        return row_id

    def select(self, query_dict):
        row_list = self.collection.find(query_dict)
        return row_list

    def select_one(self, query_dict):
        row_dict = self.collection.find_one(query_dict)
        return row_dict

    def update_one(self, where_dict, update_dict):
        row_modified = self.collection.update_one(where_dict, {'$set': update_dict}).modified_count
        return row_modified

    def delete_one(self, where_dict):
        row_modified = self.collection.delete_one(where_dict).modified_count
        return row_modified
    
    def update_insert(self, where_dict, update_dict):
        row_id = self.collection.update(where_dict, update_dict, upsert=True)
        return row_id