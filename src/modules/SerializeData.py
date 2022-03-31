
class SerializeData:

    def __init__(self,data,needed_attributes):
        self.data = data
        self.needed_attributes = needed_attributes


    def serialize(self):
        result = {}
        for attr in self.needed_attributes:
            if attr == '_id':
                result[attr] = str(self.data[attr])
            else:
                result[attr] = self.data[attr]
        return result
