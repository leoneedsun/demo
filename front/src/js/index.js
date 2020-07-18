function Banner() {
    this.bannerWidth = 795
    this.bannerGruop = $("#banner_group")
    this.index = 1
    this.leftArrow = $('.left_arrow')
    this.rightArrow = $('.right_arrow')
    this.bannerUl = $('#banner_ul')
    this.liList = this.bannerUl.children('li') // childern 获取bannerUl下所有的li标签
    this.bannerCount = this.liList.length // 获取li标签的长度，即个数
    this.pageControl = $('.page_control')
}

// 动态设置Banner宽度
Banner.prototype.initBanner = function () {
    var self = this

    // 设置第一个和最后一个Banner的复制品，顺序：3，1，2，3，1
    // eq():获取第几个标签
    // clone():克隆
    var firstBanner = self.liList.eq(0).clone()
    var lastBanner = self.liList.eq(self.bannerCount - 1).clone()

    // append():在位置最后添加指定标签
    // prepend():在位置最前添加指定标签
    self.bannerUl.append(firstBanner)
    self.bannerUl.prepend(lastBanner)

    // 设置bannerUl的宽度，也就是3，1，2，3，1的宽度
    // 因为Banner顺序为3，1，2，3，1，所以要设置1为起始位置，即'left':-self.bannerWidth
    self.bannerUl.css({'width': self.bannerWidth * (self.bannerCount + 2), 'left': -self.bannerWidth})
}

// 设置Banner上初始化原点
Banner.prototype.initPageControl = function () {
    var self = this

    // 添加for循环
    for (var i = 0; i < self.bannerCount; i++) {
        var circle = $('<li></li>') // 添加 li 标签，如果是 $('li') 则是获取网页中所有 li 元素
        self.pageControl.append(circle)
        if (i === 0) {
            circle.addClass('active')
        }
    }
    // 动态设置Banner上小圆点区域宽度
    self.pageControl.css({'width': self.bannerCount * 12 + 8 * 2 + 16 * (self.bannerCount - 1)})
}

// 设置Banner左右箭头显示/隐藏的效果
Banner.prototype.toggleArrow = function (isShow) {
    var self = this
    if (isShow) {
        self.leftArrow.show()
        self.rightArrow.show()
    } else {
        self.leftArrow.hide()
        self.rightArrow.hide()
    }

}

// 设置轮播运行
Banner.prototype.animate = function () {
    var self = this
    // bannerUl.css({'left':-795}); 缺点：一步到位
    self.bannerUl.stop().animate({"left": -795 * self.index}, 500);

    // 设置Banner上小圆点与图片同步切换
    var index = self.index
    if (index === 0) {
        index = self.bannerCount - 1
    } else if (index === self.bannerCount + 1) {
        index = 0
    } else {
        index = self.index - 1
    }

    // eq:代表获取第几个 li 标签，eq(self.index)表示获取第index个
    // siblings 是找到 active 外其他的兄弟元素
    self.pageControl.children('li').eq(index).addClass('active').siblings().removeClass('active')
}

// 设置Banner循环
Banner.prototype.loop = function () {
    var self = this
    this.timer = setInterval(function () {
        if (self.index >= self.bannerCount + 1) {
            self.bannerUl.css({'left': -self.bannerWidth})
            self.index = 2;
        } else {
            self.index++;
        }
        self.animate()
    }, 2000)
}

// 监听：控制Banner左右箭头点击翻页效果
Banner.prototype.listenArrowClick = function () {
    var self = this
    // 左侧箭头
    self.leftArrow.click(function () {

        // ==: 1 == '1' 返回的是true
        // ===: 1 != '1' 返回的是数值
        if (self.index === 0) {
            self.bannerUl.css({'left': -self.bannerCount * self.bannerWidth})
            self.index = self.bannerCount - 1
        } else {
            self.index--
        }
        self.animate()
    })

    //右侧箭头
    self.rightArrow.click(function () {
        if (self.index === self.bannerCount + 1) {
            self.bannerUl.css({'left': -self.bannerWidth})
            self.index = 2
        } else {
            self.index++
        }
        self.animate()
    })
}

// 监听：设置鼠标在Banner移入/移除时，左右箭头显示/隐藏
Banner.prototype.listenBannerHover = function () {
    var self = this
    this.bannerGruop.hover(function () {
        // 第一个函数是把鼠标移动到banner上会执行的函数
        clearInterval(self.timer)
        self.toggleArrow(true)

    }, function () {
        // 第二次函数是把鼠标从banner上移走会执行的函数
        self.loop()
        self.toggleArrow(false)
    })
}

// 监听：设置Banner上小圆点的点选和循环效果
Banner.prototype.listenPageControl = function () {
    var self = this

    // children('li')获取pageControl下所有li的子节点，each()遍历所有的li标签，再指定function(index,obj)
    // obj 为 li 标签本身
    self.pageControl.children('li').each(function (index, obj) {

        // 打印看一下index和obj是什么
        // console.log(index)
        // console.log(obj)
        // console.log('====================')

        // 只有将 obj 包装成 jquery 方法才可以添加 click 方法
        $(obj).click(function () {
            self.index = index
            self.animate()
        })
    })
}

// 载入Banner运行方式
Banner.prototype.run = function () {
    this.initBanner()
    this.initPageControl()
    this.loop()
    this.listenArrowClick()
    this.listenBannerHover()
    this.listenPageControl()
};

function Index() {
    var self = this
    self.page = 2
    self.category_id = 0
    self.loadBtn = $('#load-more-btn')
}

Index.prototype.listenLoadMoreEvent = function () {
    var self = this
    var loadBtn = $("#load-more-btn")
    loadBtn.click(function () {
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'p': self.page,
                'category_id': self.category_id
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var newses = result['data']
                    if (newses.length > 0) {
                        var tpl = template('news-item', {'newses': newses})
                        var ul = $('.list_inner_group')
                        ul.append(tpl)
                        self.page += 1
                    } else {
                        loadBtn.hide()
                    }
                }
            }
        })
    })
}

Index.prototype.listenCategorySwitchEvent = function () {
    var self = this
    var tabGroup = $('.list_tab')

    // children可以获得该标签下所有的子元素
    tabGroup.children().click(function () {
        // this 代表当前选中的这个li标签
        var li = $(this)
        var category_id = li.attr('data-category')
        var page = 1
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'category_id': category_id,
                'p': page
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var newses = result['data']
                    var tpl = template('news-item', {'newses': newses})

                    // empty:可以将这个标签下的所有子元素都删掉
                    var newsListGroup = $('.list_inner_group')
                    newsListGroup.empty()
                    newsListGroup.append(tpl)
                    self.page = 2
                    self.category_id = category_id

                    // siblings 用来获得兄弟元素
                    li.addClass('active').siblings().removeClass('active')
                    self.loadBtn.show()
                }
            }
        })
    })
}

Index.prototype.run = function () {
    var self = this
    self.listenLoadMoreEvent()
    self.listenCategorySwitchEvent()
}

// 设置html全部渲染后再执行上述指令
$(function () {
    var banner = new Banner();
    banner.run();

    var index = new Index()
    index.run()
});