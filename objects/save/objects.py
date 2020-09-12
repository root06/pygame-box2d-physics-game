import json, pickle

class Save(object):
    def __init__(self, db, default_file):
        self.database = db
        self.default = default_file
        self.data = self.__read()
    
    def change_db(self, new_db):
        self.database = new_db 

    def load(self, result_type="obj"):
        self.data = self.__read()
        if result_type == "obj":
            print(self.data)
            return SaveObject(self.data)

        if result_type == "dict":
            return eval(self.data)

        if result_type == "json":
            return json.loads(self.data)

        if result_type == "string":
            return self.data    

    def write(self, change_data=None):
        if change_data:
            self.data = change_data
        self.__write()

    def __write(self):
        pickle.dump(self.data,open(self.database, "wb" ))
    def __read(self):
        try:
            return pickle.load(open(self.database, "rb" ))
        except FileNotFoundError:
            return pickle.load(open(self.default, "rb" ))
    
class SaveObject:
    def __init__(self, dat):
        self.__dict__.update(dat)