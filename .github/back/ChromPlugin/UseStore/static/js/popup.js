// 立即执行函数
(function () {
  console.log('立即执行函数');
  // 请求地址
  // get1024Home()
  initEvent()
  // 获取我的IP地址
  getMyaddress()
  // 数据存储先回显
  showTotal()
  handleCookie()
  // 添加增加事件
  const save = document.getElementById('save')
  console.log('save----', save);
  save.onclick = function () {
    console.log('存储数据');
    chrome.storage.sync.get("total", function (res) {
      var totalAmount = 0;
      if (res.total) {
        totalAmount = parseFloat(res.total)
      }
      var saile = document.getElementById("sail")
      // 将总金额设置为totalAmount
      var money = document.getElementById("money")
      var total = totalAmount + parseFloat(saile.value)
      money.innerHTML = total;
      // 最后存储到total中
      chrome.storage.sync.set({ total }, () => {
        saile.value = ""
        console.log('set successed!');
      });
    })
  }

  // 当前激活的tabUrl
  let tabUrl = null
  let tabCookies = null

  // 获取网站的cookie和useragent，并打印出来
  function handleCookie() {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
      let url = tabUrl || tabs[0].url;
      tabUrl = url;
      // use `url` here inside the callback because it's asynchronous!
      console.log('url--', url);
      chrome.cookies.getAll({ url }, function (cookies) {
        console.log('得到的Cookie是：', cookies);
        tabCookies = cookies;
        const resList = cookies.map(item => {
          return `${item.name}=${item.value}`
        })
        const cookieStr = resList.join("; ")
        console.log("cookies-----", cookieStr);
        document.getElementById("cookies").innerHTML = cookieStr
        document.getElementById("useragent").innerHTML = navigator.userAgent
      });
    });
  }


  // 检测Cookie发生变化
  // chrome.cookies.onChanged.addListener((changeInfo) => {
  //   console.log('cookie发生变化了', changeInfo);
  //   var cookieKey = changeInfo.cookie.name
  //   var cookieDomain = "https://" + changeInfo.cookie.domain
  //   var cookieValue = changeInfo.cookie.value
  //   if (cookieDomain === "http://localhost") {
  //     console.log('检测到localhost的cookie变化了', cookieKey);
  //   }
  //   if (cookieKey === "setDumpTarget") {
  //     console.log('检测到setDumpTarget的cookie变化了', cookieKey);
  //     const configCookie = { "url": cookieDomain, "name": "editCookit", "value": "11111111111111" }
  //     chrome.cookies.set(configCookie);
  //   }
  // })

  // 清空网站cookie
  function removeCookie() {
    console.log('removeCookieurl--', tabUrl, tabCookies);
    tabCookies.forEach(item => {
      console.log('removeCookie删除的Cookie:', item.name);
      chrome.cookies.remove({ url: tabUrl, name: item.name })
    });
    handleCookie()
  }

  // 获取1024地址
  function get1024Home() {
    var form = new FormData();
    form.append("a", "get18");
    form.append("system", "android");
    var settings = {
      "url": "https://get.xunfs.com/app/listapp.php",
      "method": "POST",
      "timeout": 0,
      "processData": false,
      "mimeType": "multipart/form-data",
      "contentType": false,
      "data": form
    };
    $.ajax(settings).done(function (response) {
      var homePath = JSON.parse(response)
      console.log("homePath----", homePath);
      var home1 = homePath.url1
      var home2 = homePath.url2
      var home3 = homePath.url3
      var homeBox = document.getElementById("home-box")
      homeBox.appendChild(getHomeA(home1))
      homeBox.appendChild(getHomeA(home2))
      homeBox.appendChild(getHomeA(home3))
    });
  }

  // 获取当前IP地址
  function getMyaddress() {
    console.log('获取我的IP地址');
    var settings = {
      "url": "http://myip.ipip.net",
      "method": "GET",
      "timeout": 0,
    };
    $.ajax(settings).done(function (response) {
      console.log("response---", response);
      const ipbox = document.getElementById("ipbox")
      ipbox.innerHTML = response
    });
  }

  function getHomeA(home) {
    var a2 = document.createElement("a")
    a2.href = `https://${home}/`
    a2.text = `https://${home}/`
    a2.target = "_blank"
    a2.className = "home1024"
    return a2
  }

  function initEvent(params) {
    // 添加清空全部事件
    const clearBtn = document.getElementById("clear-btn")
    clearBtn.onclick = function () {
      chrome.storage.sync.clear(() => {
        console.log('已清空所有内容');
        showTotal()
      })
    }
    // 添加获取地址事件
    const getHome = document.getElementById("btn-1024")
    getHome.onclick = get1024Home

    // 清空cookie
    const removeCookitBtn = document.getElementById("removeCookie")
    removeCookitBtn.onclick = removeCookie

    //点击后进行复制功能
    $('#copyCookie').click(function () {
      $('#hide').val(document.getElementById("cookies").innerText);//把要复制的内容给到这里
      $('#hide').select();
      try { var state = document.execCommand('copy'); } catch (err) { var state = false; }
      console.log('state----', state);
      if (state) {
        $("#copyCookie").text('Cookie已复制')
      } else {
        $("#copyCookie").text('Cookie复制失败')
      }
    })

    // 添加打开设置页面事件
    const openset = document.getElementById("openset")
    openset.onclick = function () {
      chrome.tabs.create({
        url: './static/views/onboarding.html'
      });
    }

    // 添加百度自动点击执行操作
    const baidu = document.getElementById("baiduauto")
    baidu.onclick = async function () {
      // 先获取当前激活的tab页
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      // 然后向这个tab页里面发送消息
      console.log('开始自动滚动: ' + tab);
      const response = await chrome.tabs.sendMessage(tab.id, { greeting: "百度滚动" });
      // do something with response here, not outside the function
      console.log(response);
    }

    // 添加抖音关注列表滚动
    const douyinGuanzhu = document.getElementById("douyinFansi")
    douyinGuanzhu.onclick = async function () {
      // 先获取当前激活的tab页
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      // 然后向这个tab页里面发送消息
      console.log('开始自动滚动: ' + tab);
      const response = await chrome.tabs.sendMessage(tab.id, { greeting: "抖音关注列表滚动" });
      // do something with response here, not outside the function
      console.log(response);
    }

    // 抖音粉丝下一页
    addButtonClickToContentMessage("nextPage", "抖音关注下一页")

    // 取消关注当前页
    addButtonClickToContentMessage("cancelPage", "取消关注这页")

    // 切换userAgent
    const toggleUserAgent = document.getElementById("toggle-useragent")
    toggleUserAgent.onclick = async function () {
      // 先获取当前激活的tab页
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      // 然后向这个tab页里面发送消息
      console.log('开始toggleUserAgent: ', tab);
      const response = await chrome.runtime.sendMessage("editUserAgent");
      // const response = await chrome.tabs.sendMessage(tab.id, { greeting: "hello" });
      // do something with response here, not outside the function
      console.log("toggleReceiveResponse:", response);
    }

    // 恢复userAgent
    const resetUserAgent = document.getElementById("reset-useragent")
    resetUserAgent.onclick = async function () {
      // 先获取当前激活的tab页
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      // 然后向这个tab页里面发送消息
      console.log('开始resetUserAgent: ', tab);
      const response = await chrome.runtime.sendMessage("resetUserAgent");
      // const response = await chrome.tabs.sendMessage(tab.id, { greeting: "hello" });
      // do something with response here, not outside the function
      console.log("resetUserAgentReceiveResponse:", response);
    }
  }

  // 初始化总金额
  function showTotal(params) {
    chrome.storage.sync.get("total", function (res) {
      if (res.total) {
        totalAmount = parseFloat(res.total)
        var money = document.getElementById("money")
        money.innerHTML = totalAmount;
      } else {
        var money = document.getElementById("money")
        money.innerHTML = 0
      }
    })
  }

  function addButtonClickToContentMessage(btnId, message) {
    document.getElementById(btnId).onclick = async function () {
      // 先获取当前激活的tab页
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      // 然后向这个tab页里面发送消息
      console.log('开始addButtonClickToContentMessage: ' + tab);
      const response = await chrome.tabs.sendMessage(tab.id, { greeting: message });
      // do something with response here, not outside the function
      console.log(response);
    }
  }
})()