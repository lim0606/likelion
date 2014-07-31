class Database(object):

    def __init__(self):
        self.database = [{
            'id': 0,
            'title': "",
            'content': "",
            'datetime': "",
            'likecount': 0,
        }]

    def newid(self):
        return self.maxid() + 1

    def maxid(self):
        _id = -1
        for item in self.database:
            if _id < item['id']:
                _id = item['id']
        return _id

    def put(self, storage):
        self.database.append(storage)

    def out(self):
        return self.database

    def get_entries_10(self):
        return self.database[:10]

    def select(self, _id):
        for index, item in enumerate(self.database):
            if str(item['id']) == _id:
                return item

    def update(self, _id, value):
        for index, item in enumerate(self.database):
            if str(item['id']) == _id:
                self.database[index] = value
                break

    def delete(self, _id):
        for index, item in enumerate(self.database):
            if str(item['id']) == _id:
                self.database.pop(index)
                break
        


