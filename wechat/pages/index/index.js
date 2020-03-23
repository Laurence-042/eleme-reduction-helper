//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    shop_code: 'E10538147636171159542',
    reduction_target: 38,
    base_menu: '招牌香辣鸡腿堡',
    block_menu: '纸巾,矿泉水,红苹果,可乐,美年达,雪碧,康师傅,饮品',
    suggest: {},
    got_suggest: false
  },
  get_suggest(e) {
    console.log(e.detail.value);

    let data = e.detail.value;

    if (data.shop_code.length == 0 || data.reduction_target.length==0) {
      wx.showToast({
        title: '请填写必要内容',
        icon: 'fail',
        duration: 1000,
        mask: true
      })
      return;
    } else {
      wx.showToast({
        title: '正在生成菜单',
        icon: 'success',
        duration: 1000,
        mask: true
      })
    }
    // data.shop_code = data.shop_code.length == 0 ? this.data.shop_code : data.shop_code;
    // data.reduction_target = data.reduction_target.length == 0 ? this.data.reduction_target : data.reduction_target;
    // data.base_menu = data.base_menu.length == 0 ? this.data.base_menu : data.base_menu;
    // data.block_menu = data.block_menu.length == 0 ? this.data.block_menu : data.block_menu;

    console.log(data);
    let that = this;
    wx.request({
      url: 'https://www.laurence042.com:9043/eleme',
      data: {
        shop_code: data.shop_code,
        reduction_target: data.reduction_target,
        base_menu: data.base_menu,
        block_menu: data.block_menu
      },
      success(res) {
        let data = res.data;

        console.log(res.data);

        if (data.errMsg != null) {
          wx.showToast({
            title: errMsg,
          })
          return;
        }
        
        that.get_bill(data.suggest, data.total, data.reduction_price);
      }
    })
  },
  get_bill(foods, total, reducetion) {
    let category_foods_map = {};

    foods.forEach(food => {
      if (category_foods_map[food.category] == null) {
        category_foods_map[food.category] = [];
      }
      category_foods_map[food.category].push({
        "name": food.name,
        "price": food.price,
        "packing_fee": food.packing_fee
      })
    })

    let suggest = {
      entries: category_foods_map
    };

    suggest.total = "总花销：" + total + "-" + reducetion + "=" + (total - reducetion).toFixed(2);

    let format_suggest = ""
    for (let category in suggest.entries) {
      format_suggest += "==" + category + "==\n";
      suggest.entries[category].forEach(food => {
        format_suggest += food.name + ' ';
        format_suggest += "单价：" + food.price + ' ';
        format_suggest += "包装费：" + food.packing_fee + '\n';
      });
    }
    format_suggest += '\n' + suggest.total;
    suggest.format = format_suggest;
    console.log(suggest)

    this.setData({
      suggest: suggest,
      got_suggest: true
    });
  },
  copy_suggest(e) {
    let suggest = this.data.suggest.format;
    wx.setClipboardData({
      data: suggest,
      success(res) {
        wx.getClipboardData({
          success(res) {
            console.log(res.data) // data
          }
        })
      }
    })
  },
  clear_suggest() {
    this.setData({
      suggest: {},
      got_suggest: false
    })
  }
})