from bson.objectid import ObjectId

from driver import mongo

class Base():
    def list(self):
        documents = mongo[self.COLLECTION].find({})

        return documents

    def get(self, _id):
        _id = ObjectId(_id)

        document = mongo[self.COLLECTION].find_one({'_id' : _id})

        return document

    def count(self):
        count = mongo[self.COLLECTION].find({}).count()

        return count

    def insert(self, data):
        document = mongo[self.COLLECTION].insert(data)

        return document

    def update(self, _id, data):
        _id = ObjectId(_id)

        query = {
            '_id' : _id
        }

        del data['_id']

        update = {
            '$set' : data
        }

        document = mongo[self.COLLECTION].update_one(query, update)

        return document

    def delete(self, _id):
        _id = ObjectId(_id)

        result = mongo[self.COLLECTION].delete_one({'_id' : _id})

        if result.deleted_count == 1:
            return True
        else:
            return False