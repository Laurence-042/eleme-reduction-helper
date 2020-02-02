# -*- coding:utf-8 -*-

import json
import ssl
from urllib.error import HTTPError

from aiohttp import web

from settings import config
from util import get_suggest

routes = web.RouteTableDef()


# http://localhost:8080/eleme?shop_code=E3276789706198936889&reduction_target=35&base_menu=蜜汁烤肉拌饭+4种配菜&block_menu=纸巾,矿泉水,红苹果,可乐,美年达,雪碧,康师傅,饮品
@routes.get('/eleme')
async def hello(request):
    param = dict(request.query)
    shop_code = param.get("shop_code")
    if shop_code is None:
        res = {"errMsg": "No shop code"}
        return web.Response(text=json.dumps(res), headers={"Access-Control-Allow-Origin": "*"})
    reduction_target = int(param.get("reduction_target", 20))
    base_menu = param.get("base_menu", "").split(',')
    block_menu = param.get("block_menu", "").split(',')
    base_menu = list(filter(lambda x: x, base_menu))
    block_menu = list(filter(lambda x: x, block_menu))
    try:
        suggest, total, reduction_price = get_suggest(shop_code=shop_code, reduction_target=reduction_target,
                                                      base_menu=base_menu, block_menu=block_menu,
                                                      header_dir=config['header_dir'])
    except HTTPError as e:
        res = {"errMsg": "{} {}".format(e.code, e.reason), "reason": ["unknown"]}
        if e.code == 400:
            res['reason'] = ["shop code is not valid"]
        return web.Response(text=json.dumps(res), headers={"Access-Control-Allow-Origin": "*"})

    suggest = list(map(lambda x: x.as_dict(), suggest))
    res = {"suggest": suggest, "total": total, "reduction_price": reduction_price}
    return web.Response(text=json.dumps(res), headers={"Access-Control-Allow-Origin": "*"})


app = web.Application()
app.add_routes(routes)

if config['use_ssl']:
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(config['domain_srv_crt_dir'], config['domain_srv_key_dir'])
    web.run_app(app, host=config['host'], port=config['port'], ssl_context=ssl_context)
else:
    web.run_app(app, host=config['host'], port=config['port'])
