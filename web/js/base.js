function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

var demo = new Vue({
  el: '#demo',
  data: {
    shop_code: 'E3276789706198936889',
    reduction_target: 35,
    base_menu: '蜜汁烤肉拌饭+4种配菜',
    block_menu: '纸巾,矿泉水,红苹果,可乐,美年达,雪碧,康师傅,饮品',
    suggest: ''
  },
  mounted() {
  },
  methods: {
    get_suggest(e = undefined) {
      var that = this;
      axios.get('http://localhost:8080/eleme', {
        params: {
          shop_code: that.shop_code,
          reduction_target: that.reduction_target,
          base_menu: that.base_menu,
          block_menu: that.block_menu
        }
      })
        .then(function (response) {
          var data = response.data;

          if (data.errMsg != null) {
            that.suggest = data.errMsg;
            return;
          }

          that.get_bill(data.suggest, data.total, data.reduction_price);

          // console.log(response.data);
        })
        .catch(function (error) {
          console.log(error);
        })
    },
    get_bill(foods, total, reducetion) {
      var category = "";
      suggest = "";
      foods.forEach(food => {
        if (food.category != category) {
          category = food.category;
          suggest += "====" + category + "====\n";
        }
        suggest += food.name + " " + food.price + " 餐盒费：" + food.packing_fee + "\n";
      });
      suggest += "\n";
      suggest += "总花销：" + total + "-" + reducetion + "=" + (total - reducetion).toFixed(2);
      this.suggest = suggest;
    },
    clear_suggest(){
      this.suggest = "";
    },
    copy_url(e = undefined) {
      console.log(e);
      console.log(e.target);
      var text = e.target.innerText;
      var input = document.getElementById("copy-helper");
      input.value = text; // 修改文本框的内容
      input.select(); // 选中文本
      document.execCommand("copy"); // 执行浏览器复制命令
      alert("复制成功");
    }
  }
})