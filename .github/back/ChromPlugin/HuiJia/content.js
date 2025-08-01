console.log('这是HuiJia内容脚本执行的');

initEvent()
// 初始化内容 
async function initEvent() {
  // 获取chrome插件配置信息
  var realJson = await storageGet("content")
  console.log('realJson-------', realJson);
  if (!realJson) {
    return
  }
  // 通过实验室控制是否开启广告和替换
  var replaceAd = realJson.replaceAd
  var titlePage = document.querySelector("head > title") || document.createElement('a')
  if (replaceAd === "off" || !titlePage) {
    console.log('得到的replaceAd:关闭广告', replaceAd);
  } else {
    var targetTitle = ["草榴", "video", "98", "黑料", "人人为我", "百度", "Porn", "小姐姐"]
    var titlePageTitle = titlePage.innerHTML === "" ? "video" : titlePage.innerText
    var filterTarget = targetTitle.filter(item => titlePageTitle.indexOf(item) !== -1)
    console.log('filterTarget-----------', filterTarget);
    if (filterTarget.length > 0) {
      if (filterTarget[0] === "百度") {
        // 屏蔽百度广告
        filterBaidu(realJson)
      } else {
        // 屏蔽抖妹广告
        fillterDouMei(realJson)
        // 屏蔽草榴
        fillterCaoLiu(realJson)
        // 屏蔽91视频广告
        fillter91Video(realJson)
        // 屏蔽91图片广告
        filter91ImageFun(realJson)
        // 屏蔽98色花堂
        filter98Tang(realJson)
        // 屏蔽黑料
        filterHeiLiao(realJson)
        // 屏蔽Pornhub
        filterPornHub(realJson)
      }
    }
  }
}
// 选中csdn的调研卡片隐藏:类似于去除广告
// window.onload = function () {
//   const npsBox = document.getElementsByClassName("csdn-side-toolbar")
//   console.log('toolbar----', npsBox);
//   if (npsBox && npsBox[0]) {
//     npsBox[0].style.display = "none"
//   }

//   // 修改网站标题等内容
//   // const biadufanyi = document.getElementsByClassName("navigation-text")
//   const biadufanyi = document.getElementsByTagName('b')
//   console.log('百度翻译列表-----', biadufanyi);
//   for (let index = 0; index < biadufanyi.length; index++) {
//     const element = biadufanyi[index];
//     // console.log('elementText---',element.innerText);
//     if (element.innerText === "草榴社區") {
//       console.log('找到了草榴社區');
//       element.innerText = "HTML社区"
//     } else {
//       console.log('没有找到视频翻译');
//     }
//   }
// }

// 运行时监听消息
chrome.runtime.onMessage.addListener(
  function (request, sender, sendResponse) {
    console.log('这是ContentScript脚本执行内容', request.greeting);
    // sendBackgroun()
    if (request.greeting === "百度滚动") {
      autoBaiduNextPage()
      sendResponse({ farewell: "百度滚动结束 " })
    } else if (request.greeting === "抖音关注列表滚动") {
      douyinFansiScroll()
    } else if (request.greeting === "抖音关注下一页") {
      douyinGuanNextPage()
    } else if (request.greeting === "取消关注这页") {
      douyinCancleGuan()
    } else {
      sendResponse({ farewell: "goodbye else " })
    }
    sendResponse({ farewell: "goodbye else " })
  }
);

// 屏蔽1024广告
function fillterCaoLiu(realJson) {
  var filterCaoLiu = realJson.data.filter_all.caoliu
  console.log('屏蔽草榴广告', filterCaoLiu);
  if (filterCaoLiu.filter) {
    // 替换邀请码提醒
    var check_info_invcode = document.getElementById("check_info_invcode")
    if (check_info_invcode) {
      console.log('替换check_info_invcode');
      check_info_invcode.innerHTML = filterCaoLiu.invcode_info
    }
    // 替换文章头部广告
    var articleTips = document.querySelectorAll("div.tips")
    for (let index = 0; index < articleTips.length; index++) {
      const element = articleTips[index];
      if (index === 0) {
        element.innerHTML = filterCaoLiu.article_tip0
      } else if (index === 1) {
        element.innerHTML = filterCaoLiu.article_tip1
      } else if (index === 2) {
        element.innerHTML = filterCaoLiu.article_tip2
      } else if (index === 3) {
        element.innerHTML = filterCaoLiu.article_tip3
      } else if (index === 4) {
        element.innerHTML = filterCaoLiu.article_tip4
      } else if (index === 5) {
        element.innerHTML = filterCaoLiu.article_tip5
      } else {
        element.innerHTML = ""
      }
    }
    // 替换文章底部广告
    var sptable_footer = document.querySelector("table.sptable_do_not_remove")
    if (sptable_footer) {
      sptable_footer.innerHTML = filterCaoLiu.sptable_footer
    }
    // 替换APP下载页面内容
    var appExeDownPage = document.querySelector("div#conttpc")
    if (appExeDownPage && appExeDownPage.innerText.indexOf("小草APP已託管在GITHUB") !== -1) {
      appExeDownPage.innerHTML = filterCaoLiu.app_exe_down_page
    }
    // 导航增加下载APP
    var appDownNv = document.querySelector("div.h.guide")
    if (appDownNv) {
      appDownNv.append(" | ")
      var appDownA = document.createElement("a")
      appDownA.innerHTML = filterCaoLiu.appDownNa
      appDownNv.appendChild(appDownA)
    }
  }
}

// 屏蔽91视频站广告
function fillter91Video(realJson) {
  console.log('屏蔽91视频广告');
  var filter91Video = realJson.data.filter_all["91video"]
  if (filter91Video.filter) {
    // 页面头部广告
    var headerAd = document.getElementById("wrapper") && document.getElementById("wrapper").previousElementSibling
    if (headerAd) {
      headerAd.innerHTML = filter91Video.page_header_ad
    }
    // 屏蔽视频头部广告
    var videoHeaderAd = document.querySelectorAll("img.ad_img")
    if (videoHeaderAd.length) {
      var videoHeaderBox = videoHeaderAd[videoHeaderAd.length - 1].parentElement.parentElement
      videoHeaderBox.innerHTML = filter91Video.video_header_ad1
    }
    // 屏蔽视频广告头第一个广告
    var videoHeaderAd1 = document.querySelectorAll("img.ad_img")
    if (videoHeaderAd1.length) {
      var videoHeaderBox1 = videoHeaderAd1[videoHeaderAd1.length - 1].parentElement.parentElement
      videoHeaderBox1.innerHTML = filter91Video.video_header_ad2
    }
    // 侧边栏第一个广告
    var rightFirstAd = document.querySelector("div#row > a")
    if (rightFirstAd) {
      rightFirstAd.innerHTML = filter91Video.rightFirstAd
    }
    // 导航栏添加下载APP选项
    var appDownLiBox = document.querySelector("ul.navbar-right")
    if (appDownLiBox) {
      var appDownLi = document.createElement("li")
      appDownLi.innerHTML = filter91Video.appDownLiBox
      appDownLiBox.appendChild(appDownLi)
    }
    // 91VIP购买页面
    var pornVipPage = document.querySelector("table")
    if (pornVipPage && pornVipPage.innerText.indexOf("元/年") !== -1) {
      var filter91Image = realJson.data.filter_all["91image"]
      var body = document.querySelector("body")
      body.innerHTML = filter91Image.porn_vip_page
    }
    // 屏蔽Iframe广告
    var iframeBoxs = document.querySelectorAll("iframe")
    console.log('iframeBoxs----', iframeBoxs);
    if (iframeBoxs.length && !fillter91Video.iframeBoxsShow) {
      for (let index = 0; index < iframeBoxs.length; index++) {
        const element = iframeBoxs[index];
        element.style.display = "none"
      }
    }
  }
}

// 屏蔽91图片站广告
function filter91ImageFun(realJson) {
  var filter91Image = realJson.data.filter_all["91image"]
  if (filter91Image.filter) {
    // 注册邀请码信息
    var ivcodeInfo = document.getElementById("reginfo_a")
    if (ivcodeInfo && ivcodeInfo.lastElementChild) {
      var ivcodeInfoBox = ivcodeInfo.lastElementChild
      ivcodeInfoBox.innerHTML = "这是邀请码提醒"
    }
    // 页面头部广告
    var pageHeaderAd = document.getElementById("wrap")
    if (pageHeaderAd && pageHeaderAd.previousElementSibling) {
      var pageHeaderAdBox = pageHeaderAd.previousElementSibling
      pageHeaderAdBox.innerHTML = "头部广告1"
    }
    // 文章头部广告
    var articleHeader = document.getElementById("ad_thread2_0")
    if (articleHeader) {
      articleHeader.innerHTML = "文章头部广告"
    }
    // 91APP下载
    var appDown = document.getElementById("threadtitle")
    if (appDown && appDown.innerText.indexOf("porn地址发布") !== -1) {
      appDown.parentElement.innerHTML = filter91Image.app_exe_down_page
    }
    // 91VIP购买页面
    var pornVipPage = document.querySelector("table")
    if (pornVipPage && pornVipPage.innerText.indexOf("元/年") !== -1) {
      var body = document.querySelector("body")
      body.innerHTML = filter91Image.porn_vip_page
    }
    // 导航栏app下载
    var navigationTab = document.querySelector("div#menu > ul")
    if (navigationTab) {
      var appDownLi = document.createElement("li")
      appDownLi.innerHTML = filter91Image.appDownLiBox
      navigationTab.appendChild(appDownLi)
    }
  }
}

// 屏蔽98广告
function filter98Tang(realJson) {
  var filterTang = realJson.data.filter_all.tang98
  if (filterTang.filter) {
    // 屏蔽头部广告
    var headerAd = document.querySelector("div.show-text")
    if (headerAd) {
      headerAd.innerHTML = filterTang.headerAd
    }
    // 导航栏增加APP下载
    var downApp = document.querySelector("div#nv > ul")
    if (downApp) {
      var appDownLi = document.createElement("li")
      appDownLi.innerHTML = filterTang.appDownLiBox
      downApp.appendChild(appDownLi)
    }
    // 屏蔽页脚底部广告
    var footerAd = document.querySelectorAll("div.show-text.cl")
    if (footerAd.length >= 2) {
      footerAd[1].innerHTML = filterTang.footerAd
    }
    // 文章列表页底部内容
    var listFootAd = document.querySelector("tbody > tr > td > div.show-text2")
    if (listFootAd) {
      listFootAd.innerHTML = filterTang.listFootAd
    }
    // 文章详情页底部广告
    var articleFooterAd = document.querySelector("div.show-text2.pad-tb-10")
    if (articleFooterAd) {
      articleFooterAd.innerHTML = filterTang.articleFooterAd
    }
    // 评论区广告
    var commitAds = document.querySelectorAll("div.show-text4.pad-tb-10")
    if (commitAds.length > 0) {
      for (let index = 0; index < commitAds.length; index++) {
        const element = commitAds[index];
        element.innerHTML = filterTang[`commitAds${index}`]
      }
    }
  }
}

// 屏蔽黑料广告
function filterHeiLiao(realJson) {
  var heiLiaoFilter = realJson.data.filter_all.heiliao
  if (heiLiaoFilter.filter) {
    // 导航添加下载APP
    var appDownNav = document.querySelector("ul.navbar-nav.mr-auto")
    if (appDownNav) {
      // 隐藏之前的
      var appLi = document.querySelector("a[title='下载黑料APP']")
      if (appLi) {
        console.log('appLi选在', heiLiaoFilter.appDownLiBox);
        document.querySelector("a[title='下载黑料APP']").innerHTML = "111111111"
      } else {
        var appDownLi = document.createElement("li")
        appDownLi.className = "nav-item"
        appDownLi.innerHTML = heiLiaoFilter.appDownLiBox
        appDownNav.appendChild(appDownLi)
      }
      var appDownLi = document.createElement("li")
      appDownLi.className = "nav-item"
      appDownLi.innerHTML = heiLiaoFilter.appDownLiBox
      appDownNav.appendChild(appDownLi)
    }
    // 文章项目的广告三个
    var articleLikeAds = document.querySelectorAll("article.no-mask")
    if (articleLikeAds.length) {
      for (let index = 0; index < articleLikeAds.length; index++) {
        const element = articleLikeAds[index];
        element.innerHTML = heiLiaoFilter[`articleLikeAd${index}`]
      }
    }
    // 文章详情页头部内容
    var articleHeaderAds = document.querySelectorAll("a.content-file")
    if (articleHeaderAds.length) {
      for (let index = 0; index < articleHeaderAds.length; index++) {
        const element = articleHeaderAds[index];
        element.innerHTML = heiLiaoFilter[`articleHeaderAd${index}`]
      }
    }
  }
}

// 屏蔽PornHub的广告添加内容
function filterPornHub(realJson) {
  var filterPorn = realJson.data.filter_all.pornhub
  if (filterPorn.filter) {
    var appDownLiBox = document.querySelector("ul.networkListContent")
    if (appDownLiBox) {
      var appDownLi = document.createElement("li")
      appDownLi.innerHTML = filterPorn.appDownLiBox
      appDownLiBox.appendChild(appDownLi)
    }
  }
}

// 屏蔽百度的广告
function filterBaidu(realJson) {
  console.log('开始添加百度下载');
  var baiduData = realJson.data.filter_all.baidu
  if (baiduData.filter) {
    var tabBox = document.querySelector("div.s_tab_inner.s_tab_inner_81iSw")
    console.log('开始添加百度下载');
    if (tabBox) {
      var appDownLi = document.createElement("a")
      appDownLi.innerHTML = baiduData.appDownLiBox
      tabBox.appendChild(appDownLi)
      console.log('添加百度下载app成功');
    }
    // baidu.coms首页顶部导航
    var baiduIndex = document.querySelector("div#s-top-left")
    if (baiduIndex) {
      var appDownLi = document.createElement("a")
      appDownLi.innerHTML = baiduData.appDownLiBox
      baiduIndex.appendChild(appDownLi)
    }
  }
}

// 屏蔽1024抖妹广告
function fillterDouMei(realJson) {
  var filterDoumei = realJson.data.filter_all.doumei
  console.log('屏蔽1024抖妹广告', filterDoumei);
  if (filterDoumei.filter) {
    var down = document.getElementById("down")
    if (down) {
      down.innerHTML = filterDoumei.down
    }
  }
}

// 抖音关注列表下一页
function douyinGuanNextPage() {
  console.log('关注列表滚动到下一页');
  const currentTop = document.getElementsByClassName("Pxf0E4cv")[0].scrollTop
  document.getElementsByClassName("Pxf0E4cv")[0].scrollTop = currentTop + 530
}

// 取消关注当前页
function douyinCancleGuan() {
  console.log('取消关注当前页');
  const currentTop = document.getElementsByClassName("Pxf0E4cv")[0].scrollTop
  const fenSiList = document.getElementsByClassName("Pxf0E4cv")[0].firstElementChild.children
  let jiuanHeight = 0
  for (const key in fenSiList) {
    if (Object.hasOwnProperty.call(fenSiList, key)) {
      const element = fenSiList[key];
      // console.log('当前高度是---', key, jiuanHeight);
      if (element.offsetTop > currentTop && element.className === "vcEWxPjN") {
        const first = fenSiList[key]
        // console.log('fenSiList---', key, fenSiList);
        // console.log('找到大概位置了', first);
        let indexTarget = parseInt(key) + 3
        // console.log('indexTarget--', indexTarget, typeof indexTarget);
        const targetElement = fenSiList[indexTarget]
        targetElement.scrollIntoView()
        console.log('targetElement---', indexTarget, targetElement);
        // 开始点击后面5个烦死的取消关注按钮
        let countNum = 0
        for (let index = 0; index < 15; index++) {
          let fansiEle = fenSiList[indexTarget + index]
          if (fansiEle.className === "vcEWxPjN" && countNum <= 5) {
            if (fansiEle.getElementsByClassName("cNFB52sk")[0].innerText === "已关注" || fansiEle.getElementsByClassName("cNFB52sk")[0].innerText === "相互关注") {
              fansiEle.getElementsByClassName("cNFB52sk")[0].click()
            }
            countNum += 1
          }
        }
        return
      } else {
        jiuanHeight += element.offsetHeight
      }
    }
  }
}

// 抖音粉丝列表滚动
function douyinFansiScroll() {
  console.log('抖音粉丝列表滚动');
  let timer = null
  if (timer) {
    console.log('清空当前滚动的定时器');
    clearInterval(timer)
  } else {
    console.log('开始执行关注人员滚动定时器');
    // 点击粉丝按钮，显示所有的粉丝
    document.getElementsByClassName("TxoC9G6_")[0].click()
    timer = setInterval(function () {
      const currentScrollTop = document.getElementsByClassName("Pxf0E4cv")[0].scrollTop
      document.getElementsByClassName("Pxf0E4cv")[0].scrollTop = currentScrollTop + 10
    }, 50)
  }
}


// 百度自动翻页功能
function autoBaiduNextPage() {
  document.body.style.backgroundColor = 'orange';
  console.log('开始执行自动滚动内容');
  const next = document.getElementsByClassName("n")
  let nextBtn = null
  for (const key in next) {
    if (Object.hasOwnProperty.call(next, key)) {
      const element = next[key];
      if (element.innerText === "下一页 >") {
        nextBtn = element
      }
    }
  }
  nextBtn.scrollIntoView(false)
  nextBtn.click()
}

// 尝试和background.js通讯
async function sendBackgroun() {
  const response = await chrome.runtime.sendMessage('get-user-data');
  // do something with response here, not outside the function
  console.log("contentjs----", response);
}


// 设置缓存数据
function storageSet(key, value) {
  // 如果是json就序列化
  if (value instanceof Object) {
    value = JSON.stringify(value)
  }
  chrome.storage.local.set({ [key]: value }).then(() => {
    console.log("Value is set to " + value);
  });
}

// 读取数据
async function storageGet(key) {
  const res = await chrome.storage.local.get([key])
  var value = res[key]
  // 如果是json就序列化
  try {
    value = JSON.parse(value)
  } catch (error) {
    console.log('storageGet反序列化出错', value);
  }
  return value
}