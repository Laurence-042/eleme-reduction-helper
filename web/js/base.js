function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

var demo = new Vue({
  el: '#demo',
  data: {
    shop_code: 'E10538147636171159542',
    reduction_target: 38,
    base_menu: '招牌香辣鸡腿堡',
    block_menu: '纸巾,矿泉水,红苹果,可乐,美年达,雪碧,康师傅,饮品',
    suggest: null,
    got_suggest: false
  },
  mounted() {
  },
  methods: {
    get_suggest(e = undefined) {
      TweenLite.to("#card-list", 0.5, {
        top: "-500%",
      });

      var that = this;
      axios.get('http://localhost:9043/eleme', {
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
            that.handle_exception(data);
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
      var category = '';
      var suggest = {};
      suggest.entries = []
      var entry = {}
      foods.forEach(food => {
        if (food.category != category) {
          category = food.category;
          entry={};
          entry.category = "=="+category+"==";
          entry.foods = [];
          suggest.entries.push(entry)
        }
        entry.foods.push({"name":food.name,"price":food.price,"packing_fee":food.packing_fee})
      });
      suggest.total ="总花销：" + total + "-" + reducetion + "=" + (total - reducetion).toFixed(2);
      this.suggest = suggest;
      this.got_suggest = true;

      setTimeout(function () {
        TweenLite.to("#card-list", 0.5, {
          top: "0em",
        });
      }, 500);
    },
    handle_exception(err){
      console.log(err);

      var suggest = {};
      suggest.entries = [];
      suggest.entries.push({category:"发生了错误，可能原因如下"})
      err.reason.forEach(reason => {
        suggest.entries.push({category:reason})
      });
      suggest.total = err.errMsg;
      this.suggest = suggest;
      this.got_suggest = true;

      setTimeout(function () {
        TweenLite.to("#card-list", 0.5, {
          top: "0em",
        });
      }, 500);
    },
    clear_suggest() {
      var that = this;
      var tl = new TimelineLite();

      tl.to("#card-list", 0.5, {
        top: "-50em",
        onComplete: function () {
          that.got_suggest = false;
          that.suggest = null;
        }
      });
      tl.to("#card-list", 0.5, {
        top: "0em",
      });
    },
    copy_suggest(e ) {
      var text = document.querySelector("#suggest").innerText;
      var input = document.getElementById("copy-helper");
      input.value = text; // 修改文本框的内容
      input.select(); // 选中文本
      document.execCommand("copy"); // 执行浏览器复制命令
      alert("复制成功");
    }
  }
})