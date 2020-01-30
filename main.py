import io
from urllib import request
import gzip
import json
import os

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

for menu_entry in data['menu']:
    print("====" + menu_entry['name'] + "====")
    for food in menu_entry['foods']:
        print(food['name'], food['lowest_price'], end=' ')
        if len(food['specfoods']) != 1:
            pass  # TODO: what if amount of specfoods larger than 1?
        for spec in food['specfoods']:
            if spec['original_price'] is not None:
                print("原价", spec['original_price'], end=' ')
                print("限{0}份".format(spec['activity']['applicable_quantity']), end=' ')
            print("餐盒费", spec['packing_fee'])
