# -*- coding: utf-8 -*-
from datetime import datetime
from bson.objectid import ObjectId

import pymongo
import config
from constant import *
from Object.database_service_base import BaseDBService
import utils.data_handler as data_handler


# from constant import DataExtraParameter, HistoryTable


class MongoDBService(BaseDBService):
    def __init__(self, database_address, database_name):
        # super(MongoDB, self).__init__(database_address, database_name)
        BaseDBService.__init__(self, database_address, database_name)
        self._client = pymongo.MongoClient(database_address)
        self._database = self._client[database_name]

    @property
    def id_name(self):
        return "_id"

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, database_address):
        self._client = pymongo.MongoClient(database_address)

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database_name, client_obj=None):
        if client_obj is None:
            self._database = self._client[database_name]
        else:
            self._database = client_obj[database_name]

    # def table(self, table_name=None, database=None):
    #     if table_name is None:
    #         return self._table
    #     else:
    #         if database is None:
    #             self._table = self._database[table_name]
    #         else:
    #             self._table = database[table_name]
    #         return self._table

    def get_available_contents_from(self, table_name):
        data = self.get_contents_from(table_name)
        data_temp = data_handler.remove_disable_datum(data)
        return data_temp

    def get_contents_from(self, table_name):
        table = self._database[table_name]
        data = self.__to_list(table.find())
        return data

    def __to_list(self, cursor):
        data = []
        for curs in cursor:
            data.append(curs)
        return data

    def insert(self, table_name, data):
        table = self._database[table_name]
        inserted_id = table.insert_one(data)
        return inserted_id

    def query(self, table_name, my_query: dict, query_filter=None):
        if self.id_name in my_query.keys() and isinstance(my_query[self.id_name], str):
            my_query[self.id_name] = ObjectId(my_query[self.id_name])
        table = self._database[table_name]
        return table.find(my_query, query_filter)

    def update(self, table_name, data_id, data: dict):
        table_name = self._database[table_name]
        my_query = {self.id_name: data_id}
        return table_name.update_one(my_query, {"$set": data})

    def delete(self, table_name, data_id):
        table_name = self._database[table_name]
        my_query = {self.id_name: data_id}
        return table_name.delete_one(my_query)

    def backup_old_data(self, origin_table_name, history_table_name, res_id, operation):
        my_query = {self.id_name: res_id}
        old_data = self.query(origin_table_name, my_query)[0]
        old_data[DataExtraParameter_1.OPERATION] = operation
        old_data[DataExtraParameter_1.DATE] = datetime.now()
        del old_data[self.id_name]
        inserted_id = self.insert(history_table_name, old_data).inserted_id
        return old_data


class DataClient:
    _db_name = None

    def __init__(self, data_source_type):
        if data_source_type == "MongoDB":
            self._db_client = pymongo.MongoClient(config.MongoDB_address)
        else:
            print("NOT MongoDB")

    def get_db(self, db_name):
        self._db_name = db_name
        return self._db_client[db_name]


if __name__ == '__main__':
    print("welcome")
    db_service = MongoDBService(config.MongoDB_address, 'HCCN')
    client = db_service.client
    db = db_service.database
    contents = db_service.get_available_contents_from('rest')
    for content in contents:
        print(content)
