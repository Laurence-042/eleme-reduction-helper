from util import get_food_list_and_reduction, get_min_sum_above_floor, print_foods, print_reduction

shop_code = "E1176052134539768938"
header_dir = "./header"
param_dir = "./param"

reduction_target = 38

food_ls, reduction_ls = get_food_list_and_reduction(shop_code=shop_code, header_dir=header_dir, param_dir=param_dir)
print_reduction(reduction_ls)
print_foods(food_ls)

food_ls = list(filter(lambda x: not x.no_reduction and x.price != 0, food_ls))

reduction_price = 0
for floor, reduce in reduction_ls:
    if floor > reduction_target:
        break
    reduction_price = reduce

price_ls = list(map(lambda x: round(100 * (x.price + x.packing_fee)), food_ls))
total, index_ls = get_min_sum_above_floor(price_ls, reduction_target * 100)
total /= 100

food_suggest_ls = list(map(lambda x: food_ls[x], index_ls))
print("===建议===")
print_foods(food_suggest_ls)
print("总花销：%.2f-%.2f=%.2f" % (total, reduction_price, total - reduction_price))
