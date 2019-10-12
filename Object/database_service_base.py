# from abc import ABCMeta, abstractmethod


# class DataBase(metaclass=ABCMeta):
class BaseDBService:
    def __init__(self, database_address, database_name):
        self._database_address = database_address
        self._client = None
        self._database = None
        self._database_name = database_name
        # self._table = None

    @property
    def id_name(self):
        pass

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, database_address):
        print("No implement")

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database_name, client=None):
        print("No implement")

    @property
    def database_name(self):
        return self._database_name

    @property
    def database_name(self):
        return self._database_name

    def get_available_contents_from(self, table_name):
        pass

    def get_contents_from(self, table_name):
        pass

    def insert(self, table_name, data):
        pass

    def update(self, table_name, data_id, data):
        pass

    def backup_old_data(self, origin_table_name, history_table_name, res_id, operation):
        pass
