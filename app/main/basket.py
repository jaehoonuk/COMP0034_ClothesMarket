# Author: Jaehoon Lim

import json

class Basket:
    def __init__(self, oldBasket=None):
        if oldBasket:
            jsonObj = json.loads(oldBasket)
            self.items = jsonObj['items']
            self.totalQuantity = jsonObj['totalQuantity']
            self.totalPrice = jsonObj['totalPrice']
        else:
            self.items = {}
            self.totalQuantity = 0
            self.totalPrice = 0

    def addItem(self, item):
        id = str(item.itemId)
        if id in self.items.keys():
            self.items[id]['quantity'] += 1
            print(self.items[id]['quantity'])
            self.items[id]['price'] = self.items[id]['item']['price'] * self.items[id]['quantity']
        else:
            self.items[id] = {'item': { 'itemId': item.itemId, 'userId': item.userId, 'manufacturer': item.manufacturer, 'productName': item.productName, 'category': item.category, 'imageUrl': item.imageUrl, 'price': item.price, 'quantity': item.quantity }, 'quantity': 1, 'price': item.price}

        self.totalQuantity += 1
        self.totalPrice += self.items[id]['item']['price']

    def removeItem(self, itemId):
        id = str(itemId)
        self.totalQuantity -= self.items[id]['quantity']
        self.totalPrice -= self.items[id]['price']
        del self.items[id]

    def generateArray(self):
        arr = []
        for id in self.items:
            arr.append(this.items[id])
        return arr

    def groupBySeller(self):
        collection = self.generateArray()
        val = 0
        index = 0
        values = []
        result = []
        for i in range(len(collection)):
            val = collection[i]['item']['userId']
            try:
                index = values.index(val)
                result[index].push(collection[i])
            except ValueError:
                values.push(val)
                result.push([collection[i]])

        return result

    def serialize(self):
        return json.dumps(self.__dict__)