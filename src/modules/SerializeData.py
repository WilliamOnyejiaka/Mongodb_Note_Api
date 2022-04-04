
class SerializeData:

    def __init__(self,needed_attributes):
        # self.data = data
        self.needed_attributes = needed_attributes

    def serialize(self, data):
        result = {}
        for attr in self.needed_attributes:
            if attr == '_id':
                result[attr] = str(data[attr])
            else:
                result[attr] = data[attr]
        return result

    def dump(self,data_list):
        result = []
        for index in range(len(data_list)):
            data = self.serialize(data_list[index])
            result.append(data)
        return result
        
