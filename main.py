import re

from util import get_food_list_and_reduction, get_min_sum_above_floor, print_foods, print_reduction

shop_code = "E3276789706198936889"
header_dir = "./header"
param_dir = "./param"

reduction_target = 35
base_menu = ["蜜汁烤肉拌饭+4种配菜"]
block_menu = ["纸巾", "矿泉水", "红苹果", "可乐", "美年达", "雪碧", "康师傅", "饮品"]

food_ls, reduction_ls = get_food_list_and_reduction(shop_code=shop_code, header_dir=header_dir, param_dir=param_dir)
for block_entry in block_menu:
    pattern = ".*" + block_entry + ".*"
    food_ls = list(filter(lambda x: not re.match(pattern, x.name), food_ls))
print_reduction(reduction_ls)
print_foods(food_ls)

food_ls = list(filter(lambda x: not x.no_reduction and x.price != 0, food_ls))
base_food_ls = list(filter(lambda x: x.name in base_menu, food_ls))

base_price = 0
for base_food in base_food_ls:
    base_price += base_food.price
    food_ls.remove(base_food)

reduction_price = 0
for floor, reduce in reduction_ls:
    if floor > reduction_target:
        break
    reduction_price = reduce

price_ls = list(map(lambda x: round(100 * (x.price + x.packing_fee)), food_ls))
total, index_ls = get_min_sum_above_floor(price_ls, round((reduction_target - base_price) * 100))
total /= 100
total += base_price

food_suggest_ls = list(map(lambda x: food_ls[x], index_ls))
food_suggest_ls += base_food_ls
print("===建议===")
print_foods(food_suggest_ls)
print("总花销：%.2f-%.2f=%.2f" % (total, reduction_price, total - reduction_price))
