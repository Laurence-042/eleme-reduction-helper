# 介绍

一个简单的“饿了么”的自定义满减助手的web应用，其功能为：

- 根据商店编号自动获取满减信息与商品的类别，名称，价格等
  
    + 值得一提的是，获取商品信息过程需要登陆饿了么，但本项目暂未提供登陆的处理，只是简单地手工将登录后的cookie精简后进行get的http请求头的信息存在了header文件内供程序使用。请勿不当使用（虽然里面应该没啥个人信息）。
    
- 设定“必选”商品，必选商品一定会出现在最后的满减建议菜单中

- 设定“黑名单”词组，名称包含黑名单词组的商品将一律不出现在最后的满减建议菜单中。（比如如果黑名单中包含“饮品”，则“可口可乐饮品”“荔枝饮品”都会被加入黑名单，但“雪碧”则不会）

- 根据获取到的商品目录以及设定的满减目标，生成符合必选与黑名单设置的满减建议菜单。这个建议菜单只会尽可能让总花费超出满减目标的同时尽可能低。（比如店铺有满25减10的优惠，将满减目标设为25，则生成的菜单的总花费如果能减少到26就绝不会返回27，但也不会低于25）

    - 请不要开类似“选择一批总价格为36的必选商品，然后设定满减目标为25”这种玩笑——这种情况请直接点那些必选商品啊（死鱼眼）

# 文件介绍与部署

web目录下即为网页端源代码，其余部分为后端代码。其中config里的header存储登录信息，`config.yaml`为配置文件。

部署流程：

* 将`config.yaml`中的配置改为你的所需要的内容
* 将`js/base.js`中等唯一一个get的目标url改成你的服务器对应的url
* 将`web目录`放到nginx或apache的服务目录下，使用户可以通过80端口访问到`web/index.html`
* 使用`nohup python3 web.py &`之类的命令运行后端服务

# 现存主要问题

唯一问题差不多就是登陆饿了么拿到的SID过期后无法自动登录，因为要短信验证码。显然加个登录界面很麻烦，所以懒得动.jpg

但即使登陆实效，网页端的默认查询参数依旧可以让后端使用E10538147636171159542.json的缓存信息完成功能演示，所以这个项目还是可以长时间作为一个联合vue与python3制作web应用入门示例存在的。

如果有巨佬看到这个的话，请轻喷\_(:зゝ∠)\_ 