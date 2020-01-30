import gzip
import io
import json
import os
from urllib import request


class Food:
    name = None
    category = None
    price = 0.0
    packing_fee = 0.0
    second_price = 0.0
    applicable_quantity = 0

    def __init__(self, name, category, price, packing_fee, second_price, applicable_quantity):
        self.name = name
        self.category = category
        self.price = price
        self.packing_fee = packing_fee
        self.second_price = second_price
        self.applicable_quantity = applicable_quantity


shop_code = "E7320367095212271912"
data_dir = "./" + shop_code + ".json"
header_dir = "./header"
param_dir = "./param"
if not os.path.exists(data_dir):
    with open(param_dir, 'r') as f:
        param = f.read()
    url = "https://h5.ele.me/pizza/shopping/restaurants/" + shop_code + "/batch_shop?" + param
    with open(header_dir, 'r') as f:
        raw_header = f.read()
    header = {}
    for entry in raw_header.split('\n'):
        k, v = entry.rsplit(':', 1)
        header[k] = v
    req = request.Request(url=url, headers=header)
    response = request.urlopen(req)
    html = gzip.GzipFile(fileobj=io.BytesIO(response.read())).read().decode("utf8")

    with open(data_dir, 'w+', encoding='utf8') as f:
        f.write(html)

with open(data_dir, 'r', encoding='utf8') as f:
    html = f.read()

data = json.loads(html)
for activity_tag in data['rst']['activity_tags']:
    print(activity_tag['text'])

foods = []

for menu_entry in data['menu']:
    category = menu_entry['name']
    print("====" + category + "====")

    for raw_food in menu_entry['foods']:
        if len(raw_food['specfoods']) != 1:
            pass  # TODO: what if amount of specfoods larger than 1?

        raw_food = raw_food['specfoods'][0]

        name = raw_food['name']
        second_price = raw_food['price']
        price = second_price
        packing_fee = raw_food['packing_fee']
        applicable_quantity = 1
        if raw_food['original_price'] is not None:
            price = raw_food['original_price']
            applicable_quantity = raw_food['activity']['applicable_quantity']
        food = Food(name=name, category=category, price=price, packing_fee=packing_fee, second_price=second_price,
                    applicable_quantity=applicable_quantity)
        foods.append(food)
        print(food.name, food.second_price, end=' ')

        print("原价", food.price, end=' ')
        print("限{0}份".format(food.applicable_quantity), end=' ')
        print("餐盒费", food.packing_fee)
