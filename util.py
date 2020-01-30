import gzip
import io
import json
import os
from urllib import request

from food import Food


def get_min_sum_above_floor(nums, floor):
    n = len(nums)
    mat = [[(0, 0)] * (floor + 1) for _ in range(n)]

    for i in range(0, floor + 1):
        if i <= nums[0]:
            mat[0][i] = (nums[0], 0)
        else:
            mat[0][i] = (10000, 0)

    for i in range(1, n):
        for j in range(0, floor + 1):
            if j <= nums[i]:
                if mat[i - 1][j][0] > nums[i]:
                    mat[i][j] = (nums[i], 1)
                else:
                    mat[i][j] = (mat[i - 1][j][0], 2)
            else:
                if mat[i - 1][j - nums[i]][0] + nums[i] > mat[i - 1][j][0]:
                    mat[i][j] = (mat[i - 1][j][0], 3)
                else:
                    mat[i][j] = (mat[i - 1][j - nums[i]][0] + nums[i], 4)
    total = mat[n - 1][floor][0]

    goods = []
    cursor_x = n - 1
    cursor_y = floor
    while True:
        flag = mat[cursor_x][cursor_y][1]
        if flag == 0:
            goods.append(0)
            break
        elif flag == 1:
            goods.append(cursor_x)
            break
        elif flag == 2:
            cursor_x -= 1
            continue
        elif flag == 3:
            cursor_x -= 1
            continue
        elif flag == 4:
            goods.append(cursor_x)
            cursor_y -= nums[cursor_x]
            cursor_x -= 1
            continue
    goods = sorted(goods)

    return total, goods


def get_food_list_and_reduction(shop_code, header_dir, param_dir):
    data_dir = "./" + shop_code + ".json"

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

    reduction = []
    for activity_tag in data['rst']['activity_tags']:
        floor, reduce = map(lambda x: int(x), activity_tag['text'].split('减'))
        reduction.append((floor, reduce))

    foods = []

    for menu_entry in data['menu']:
        category = menu_entry['name']

        for raw_food in menu_entry['foods']:
            if len(raw_food['specfoods']) != 1:
                pass  # TODO: what if amount of specfoods larger than 1?

            raw_food = raw_food['specfoods'][0]

            name = raw_food['name']
            second_price = raw_food['price']
            price = second_price
            packing_fee = raw_food['packing_fee']
            applicable_quantity = 1
            no_reduction = False
            if raw_food['original_price'] is not None:
                price = raw_food['original_price']
                applicable_quantity = raw_food['activity']['applicable_quantity']
                no_reduction = True
            food = Food(name=name, category=category, price=price, packing_fee=packing_fee, second_price=second_price,
                        applicable_quantity=applicable_quantity, no_reduction=no_reduction)
            foods.append(food)

    return foods, reduction


def print_reduction(reduction_ls):
    for reduction in reduction_ls:
        print("满{0}减{1}".format(*reduction))


def print_foods(food_ls):
    food_ls = sorted(food_ls, key=lambda x: x.category + str(x.price))
    category = ""
    for food in food_ls:
        if food.category != category:
            category = food.category
            print("====" + category + "====")
        print(food.name, food.second_price, end=' ')
        print("原价", food.price, end=' ')
        print("限{0}份".format(food.applicable_quantity), end=' ')
        print("餐盒费", food.packing_fee)
