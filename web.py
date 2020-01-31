import json

from aiohttp import web

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
    suggest, total, reduction_price = get_suggest(shop_code, reduction_target, base_menu, block_menu)
    suggest = list(map(lambda x: x.as_dict(), suggest))
    res = {"suggest": suggest, "total": total, "reduction_price": reduction_price}
    return web.Response(text=json.dumps(res), headers={"Access-Control-Allow-Origin": "*"})


app = web.Application()
app.add_routes(routes)
web.run_app(app)
