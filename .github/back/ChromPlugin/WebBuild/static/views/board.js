// console.log('这是board.js文件执行的内容', document);

// 初始化事件监听
initEvent()

// 系统初始化
initConfig()

var sourceUrl = [
  "https://api.github.com/repos/1024huijia/TestSome/contents/.github/hubsql/chromHuijia.txt",
  "https://www.cnblogs.com/sdfasdf/p/15115801.html",
  "https://xiaoshen.blog.csdn.net/article/details/129345827"
]

// 获取导航地址
getChromeHuijiaData()
getExtensionData()

// 测试调用工具类的方法:ok
// sayHello()

function initConfig() {
  console.log('1024回家导航系统初始化');
}


async function sendGoogleEvent(event) {
  // 向google发送事件
  // 创建一个唯一的客户ID
  var clientId = await storageGet("clientId") || await getClientId()
  // var clientId = "GA1.1.1109513296.1677753798"
  console.log("获取到的唯一ID是:", clientId);
  const measurement_id = `G-WDMVX87J6G`;
  const api_secret = `ee_mWL4aQE6SYkmOyuIjNg`;
  try {
    fetch(`https://www.google-analytics.com/mp/collect?measurement_id=${measurement_id}&api_secret=${api_secret}`, {
      method: "POST",
      body: JSON.stringify({
        client_id: clientId,
        events: [{
          // Event names must start with an alphabetic character.
          name: event ? event : 'login',
          params: event ? {
            "content_type": "request",
            "item_id": event
          } : {
            "search_term": "search_home"
          }
        }]
      })
    }).then(res => {
      console.log('sendGoogleEvent---', res);
    });
  } catch (error) {
    console.log("send google error", error);
  }
}

// 生成唯一用户ID
const getClientId = async function () {
  // 随机数字id
  var random = Math.floor((Math.random() + Math.floor(Math.random() * 9 + 1)) * Math.pow(10, 10 - 1));
  // 时间戳
  var timeStamp = new Date().getTime();
  // clientID
  var clientId = `${random}.${timeStamp}`
  // 存储到缓存中
  await storageSet("clientId", clientId)
  return clientId
}

// 从github获取信息并解密
async function getExtensionData() {
  var settings = {
    "url": sourceUrl[0],
    "method": "GET",
    "timeout": 0,
    "headers": {
      "Accept": "application/vnd.gitapis+json",
      "X-GitHub-Api-Version": "2022-11-28"
    },
  };
  $.ajax(settings).done(async function (response) {
    sendGoogleEvent("chrome_data_success")
    var content = atob(response.content)
    var realContent = content.replaceAll("VkdWxlIGV4cHJlc3Npb25z", "")
    var realJson = JSON.parse(atob(realContent))
    if (!realJson) {
      getExtensionBokeyuan()
      sendGoogleEvent("chrome_github_error")
    } else {
      // 存储到缓存里面
      await storageSet("content", realJson)
      console.log('开始渲染地址...');
      getChromeHuijiaData()
    }
  }).fail(function () {
    // alert("请求失败，请开启或关闭代理后重试!")
    console.log("github地址获取失败...");
    getExtensionBokeyuan()
    sendGoogleEvent("chrome_github_error")
  })
}

// 从博客园获取地址并
function getExtensionBokeyuan() {
  var myHeaders = new Headers();
  myHeaders.append("authority", "www.cnblogs.com");
  myHeaders.append("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7");
  myHeaders.append("accept-language", "zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7");
  myHeaders.append("cache-control", "max-age=0");
  myHeaders.append("referer", "https://i.cnblogs.com/");
  myHeaders.append("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36");
  var requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
  };
  fetch(sourceUrl[1], requestOptions)
    .then(response => response.text())
    .then(async function (result) {
      // console.log("博客园数据:", result)
      const realContent = result.match(/VkdWxlIGV4cHJlc3Npb25z(.*?)VkdWxlIGV4cHJlc3Npb25z/)
      if (realContent && realContent.length >= 2) {
        // console.log('匹配到的内容是', realContent[1]);
        var realJson = JSON.parse(atob(realContent[1]))
        if (!realJson) {
          getExtensionCsdn()
          sendGoogleEvent("chrome_boke_error")
        } else {
          // 存储到缓存里面
          await storageSet("content", realJson)
          console.log('开始渲染地址...');
          getChromeHuijiaData()
        }
      } else {
        getExtensionCsdn()
        sendGoogleEvent("chrome_boke_error")
      }
    })
    .catch(error => {
      console.log("boke地址获取失败...")
      getExtensionCsdn()
    });
}

// 从CSDN上获取数据
function getExtensionCsdn() {
  var myHeaders = new Headers();
  myHeaders.append("authority", "xiaoshen.blog.csdn.net");
  myHeaders.append("referer", "https://mp.csdn.net/mp_blog/manage/article?spm=1011.2124.3001.5298");
  myHeaders.append("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36");
  var requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
  };
  fetch(sourceUrl[2], requestOptions)
    .then(response => response.text())
    .then(async function (result) {
      // console.log("博客园数据:", result)
      const realContent = result.match(/VkdWxlIGV4cHJlc3Npb25z(.*?)VkdWxlIGV4cHJlc3Npb25z/)
      if (realContent.length >= 2) {
        const contentReal = realContent[1].replaceAll("&#43;", "+").replaceAll("&#61;", "=")
        // console.log('CSDN匹配到的内容是', contentReal);
        var realJson = JSON.parse(atob(contentReal))
        if (!realJson) {
          alert("地址获取失败，请更换网络后重试或邮件联系:1024huijia@gmail.com")
          sendGoogleEvent("chrome_csdn_error")
        } else {
          sendGoogleEvent("chrome_csdn_success")
          // 存储到缓存里面
          await storageSet("content", realJson)
          console.log('开始渲染地址...');
          getChromeHuijiaData()
        }
      }
    })
    .catch(error => {
      console.log('cdn地址获取失败...', error)
      alert("地址获取失败，请更换网络后重试或发送邮件联系：1024huijia@gmail.com")
    });
}

// 给所有的a标签绑定发送Google事件
function aBindSendGoogle() {
  // 查询所有的a标签
  var aLinks = document.querySelectorAll("a")
  for (let index = 0; index < aLinks.length; index++) {
    const element = aLinks[index];
    element.onclick = function (e) {
      var selectItem = e.target.innerText
      console.log('选中的事件是:', selectItem);
      sendGoogleEvent(`select_${selectItem}`)
    }
  }
}

async function initEvent() {
  var realJson = await storageGet("content")
  // 芝麻开门按钮
  var openDor = document.getElementById("openDor")
  openDor.onclick = async function () {
    console.log('openDor', openDor);
    var password = document.getElementById("password")
    if (password.value === realJson.password) {
      var hidden = document.getElementById("hidden")
      hidden.style.display = "block"
      // 存储到storage中
      storageSet("password", password.value)
    } else {
      // alert("密码不正确！")
      var passwordStr = await storageGet("password")
      if (passwordStr) {
        password.value = passwordStr
      }
    }
  }

  // 其他功能按钮
  const adnone = document.getElementById("adnone") || document.createElement("a")
  adnone.onclick = (cliId) => {
    cliId.target.innerText = "还在开发中..."
  }
  // 客户端软件下载
  const clients = ["android", "windows", "macbook", "iphone", "yongjiu"]
  for (let index = 0; index < clients.length; index++) {
    const cliId = clients[index];
    const cliNode = document.getElementById(cliId)
    cliNode.onclick = async function (cliId) {
      var realJson = await storageGet("content")
      sendGoogleEvent(cliId.target.id)
      if (realJson && realJson.data[cliId.target.id]) {
        window.open(realJson.data[cliId.target.id], '_blank');
      } else {
        cliId.target.innerText = "还在开发中..."
      }
    }
  }

  // 清空本地缓存
  var clearLocalBtn = document.getElementById("clearLocal")
  clearLocalBtn.onclick = function () {
    chrome.storage.local.clear(function () {
      var error = chrome.runtime.lastError;
      if (error) {
        console.error(error);
      }
      console.log('缓存清除成功');
    });
  }

  // 关闭广告
  var offAdBtn = document.getElementById("offAd")
  offAdBtn.onclick = async function () {
    realJson.replaceAd = "off"
    storageSet("content", realJson)
  }
  // 开启广告
  var onAdBtn = document.getElementById("onAd")
  onAdBtn.onclick = async function () {
    realJson.replaceAd = "on"
    storageSet("content", realJson)
  }

}


async function initHomeUrl(chromeData) {
  // 遍历然后渲染
  var contentBox = document.getElementById("contentBox")
  // 先移除所有的内容，然后再添加导航
  contentBox.innerHTML = ""
  for (const key in chromeData.navigation) {
    if (Object.hasOwnProperty.call(chromeData.navigation, key)) {
      const element = chromeData.navigation[key];
      // console.log('elemetn', element);
      const boxTitle = element.title
      // console.log('boxTitle, boxData', boxTitle);
      // 遍历每一个tab列的内容
      if (boxTitle === "热门推荐") {
        contentBox.insertBefore(initTabBox(element), contentBox.firstChild)
      } else {
        contentBox.appendChild(initTabBox(element))
      }
    }
  }
  // 给1024地址追加刷贡献的链接
  var clAlink = document.querySelectorAll("a#caoliu")
  var currentRandom = randomInt(0, 100)
  // 获取上次刷贡献的时间
  var preTimeStamp = await storageGet("preTimeStamp") || 0
  var currentTimeStamp = new Date().getTime()
  var duringTime = currentTimeStamp - preTimeStamp
  // 3600000毫秒=3600秒=1小时
  var intervalTime = (duringTime > (3600000 * chromeData.interval))
  console.log('currentRandom, duringTime-------', currentRandom, duringTime);
  if (clAlink && chromeData.show_hotUrl && currentRandom <= chromeData.brush_rate && intervalTime) {
    // 在草榴的url上添加贡献链接
    console.log('条件成立', clAlink);
    for (let index = 0; index < clAlink.length && index < 3; index++) {
      const element = clAlink[index];
      if (element.href[element.href.length - 1] === "/") {
        console.log("chromeData.GongXians[index]----", chromeData.GongXians);
        element.href = (element.href + chromeData.GongXians[index].replace("/", ""))
      } else {
        element.href = (element.href + chromeData.GongXians[index])
      }
    }
    // 存储上次展示的时间
    storageSet("preTimeStamp", currentTimeStamp)
  } else {
    // console.log('刷贡献条件不成立', chromeData);
    console.log("clAlink && chromeData.show_hotUrl && currentRandom <= chromeData.brush_rate && duringTime > 360 * chromeData.interval", clAlink, chromeData.show_hotUrl, currentRandom <= chromeData.brush_rate, duringTime > 36 * chromeData.interval)
  }
  // 给a链接绑定发送Google事件的函数
  aBindSendGoogle()
}

// 初始化tab数据
function initTabBox(boxData) {
  var divTabBox = document.createElement("div")
  divTabBox.className = "tabBox"
  var h3Title = document.createElement("h3")
  h3Title.className = "tabTitle"
  h3Title.innerText = boxData.title
  if (boxData.title === "热门推荐") {
    h3Title.style.backgroundColor = "#006c82"
  } else {
    // h3Title.style.backgroundColor = '#' + parseInt(Math.random() * 0xFFFFFF).toString(16)
    h3Title.style.backgroundColor = "#006c82"
  }
  // url内容
  var divABox = document.createElement("div")
  divABox.className = "aBox"
  const aLinks = boxData.data
  for (const key in aLinks) {
    if (Object.hasOwnProperty.call(aLinks, key)) {
      const element = aLinks[key];
      const aTag = document.createElement("a")
      aTag.className = "alink"
      aTag.href = element.url
      aTag.target = "_blank"
      aTag.innerText = element.title
      // 给1024链接加一个标识，方便添加贡献
      if (element.title.indexOf("1024草榴") !== -1) {
        aTag.id = "caoliu"
      }
      divABox.appendChild(aTag)
    }
  }
  // 将divTabBox追加到后面
  divTabBox.appendChild(h3Title)
  divTabBox.appendChild(divABox)
  return divTabBox
}


async function getChromeHuijiaData() {
  // 从缓存中获取导航数据
  var realJson = await storageGet("content")
  if (realJson) {
    sendGoogleEvent("chrome_cache_data_success")
    // 渲染消息提醒
    initInfo(realJson)
    // 渲染导航页面
    initHomeUrl(realJson.data)
    // 给分享按钮绑定事件
    shareExtension(realJson.share)
  } else {
    sendGoogleEvent("chrome_cache_data_error")
    // alert("数据获取失败，请切换网络代理后重试或邮件联系：1024huijia@gmail.com")
  }
}


// 给分享插件按钮添加事件
function shareExtension(shareContent) {
  var shareBtn = document.getElementById("share")
  if (shareBtn) {
    shareBtn.onclick = function () {
      //把要复制的内容给到这里
      console.log('分享的的内容是', shareContent);
      sendGoogleEvent("share_chrome")
      $('#hide').val(shareContent);
      $('#hide').select();
      try { var state = document.execCommand('copy'); } catch (err) { var state = false; }
      console.log('shareExtensionstate----', state);
      if (state) {
        $("#share").text('链接已复制')
        $("#share").addClass("clicked")
      } else {
        $("#share").text('链接复制失败')
      }
      // 三秒后恢复
      setTimeout(() => {
        $("#share").text('分享插件')
        $("#share").removeClass("clicked")
      }, 5000)
    }
  }
}

// 随机生成1-100的整数
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

async function initInfo(realJson) {
  if (!realJson) {
    return
  }
  console.log("initInfo-----------", realJson);
  // 升级提醒等
  var manifest = chrome.runtime.getManifest()
  var localVersion = parseFloat(manifest.version)
  // 判断是否更新
  console.log("更新信息：---------", realJson.update.show, localVersion, realJson.version);
  if (realJson.update.show && localVersion < realJson.version) {
    alert("提示内容:" + realJson.update.content)
    chrome.storage.local.clear(function () {
      var error = chrome.runtime.lastError;
      if (error) {
        console.error(error);
      }
      console.log('缓存清除成功');
    });
    window.open(realJson.update.url)
  }
  // 判断是否弹窗
  if (realJson.dialog.show) {
    alert("提示内容:" + realJson.dialog.content)
  }
  // 嵌入更新时间
  var guideTime = realJson.data.guide_time
  if (document.getElementById("guideTime")) {
    document.getElementById("guideTime").innerHTML = guideTime
  }
  // 页面嵌入info
  var moreInfo = realJson.data.more_info
  document.getElementById("info").innerHTML = moreInfo
}

// 显示网站的cookie
function showCookie() {
  const homePaths = document.getElementsByClassName("home1024")
  const url = homePaths[0].href
  // console.log('showCookieurl--', url);
  if (!url) {
    return
  }
  chrome.cookies.getAll({ url }, function (cookies) {
    // console.log('得到的Cookie是：', cookies);
    tabCookies = cookies;
    const resList = cookies.map(item => {
      return `${item.name}=${item.value}`
    })
    const cookieStr = resList.join("; ")
    // console.log("cookies-----", cookieStr);
    document.getElementById("cookies").innerHTML = cookieStr
  });
}


// function initEvent() {
//   // 切换userAgent
//   const toggleUserAgent = document.getElementById("toggleUseragent")
//   toggleUserAgent.onclick = async function () {
//     // 先获取当前激活的tab页
//     const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
//     // 然后向这个tab页里面发送消息
//     console.log('开始toggleUserAgent: ', tab);
//     const userAgent = document.getElementById("userAgentVal").value
//     const response = await chrome.runtime.sendMessage(`editUserAgent:${userAgent}`);
//     // const response = await chrome.tabs.sendMessage(tab.id, { greeting: "hello" });
//     // do something with response here, not outside the function
//     // 切换
//     document.getElementById("useragent").innerHTML = userAgent
//     console.log("toggleReceiveResponse:", response);
//   }

//   // 恢复userAgent
//   const resetUserAgent = document.getElementById("resetUseragent")
//   resetUserAgent.onclick = async function () {
//     // 先获取当前激活的tab页
//     const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
//     // 然后向这个tab页里面发送消息
//     console.log('开始resetUserAgent: ', tab);
//     const response = await chrome.runtime.sendMessage("resetUserAgent");
//     // const response = await chrome.tabs.sendMessage(tab.id, { greeting: "hello" });
//     // do something with response here, not outside the function
//     console.log("resetUserAgentReceiveResponse:", response);
//     document.getElementById("useragent").innerHTML = navigator.userAgent
//   }

//   // 修改Cookie
//   const editBtn = document.getElementById("editCookie")
//   editBtn.onclick = function () {
//     let cookieStr = document.getElementById("cookieVal").value
//     const cookie = cookieStr.replaceAll("'", "").replaceAll("ismob=1", "ismob=0")
//     console.log('获取cookieVal---', cookie, typeof cookie);
//     if (!cookie) {
//       return
//     }
//     const cookieList = cookie.split(";")
//     cookieList.forEach(item => {
//       const keyVal = item.trim().split("=")
//       setCookie("https://cl.6273x.xyz", keyVal[0], keyVal[1])
//     })
//     console.log('修改成功');
//   }

//   // 添加获取地址事件
//   const getHome = document.getElementById("btn-1024")
//   getHome.onclick = get1024Home

//   // 同步数据按钮
//   const asyncDataBtn = document.getElementById("asyncBtn")
//   asyncDataBtn.onclick = function () {
//     console.log('开始同步数据');
//     const dataKey = document.getElementById("dataKey").value
//     const dataVal = document.getElementById("asyncData").value
//     dataVal && asyncSetData(dataKey, dataVal)
//   }

//   const asyncGetDataBtn = document.getElementById("asyncGetBtn")
//   asyncGetDataBtn.onclick = function () {
//     console.log('开始获取并展示数据');
//     const dataKey = document.getElementById("dataKey").value
//     asyncGetData(dataKey)
//   }

//   // 清空所有的同步数据
//   const clearDataBtn = document.getElementById("clearAsyncBtn")
//   clearDataBtn.onclick = function () {
//     const dataKey = document.getElementById("dataKey").value
//     clearData(dataKey)
//   }

//   // 下拉框值变化事件
//   const userAgentSel = document.getElementById("userAgentSel")
//   userAgentSel.onchange = function (e) {
//     const val = document.getElementById("userAgentSel").value
//     console.log('UserAgent下拉框变化了：', val);
//     document.getElementById("useragent").innerHTML = val
//     document.getElementById("userAgentVal").value = val
//   }

//   // 检测Cookie发生变化
//   chrome.cookies.onChanged.addListener((changeInfo) => {
//     console.log('cookie发生变化了', changeInfo);
//   })

// }


// 检测Cookie发生变化

// 存储和读取store中的数

// 存储数据
function storageSet(key, value) {
  // 如果是json就序列化
  if (value instanceof Object) {
    value = JSON.stringify(value)
  }
  chrome.storage.local.set({ [key]: value }).then(() => {
    console.log("Value is set to ");
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
    console.log('storageGet反序列化出错', key, value);
  }
  return value
}


function clearData(key) {
  if (key) {
    chrome.storage.sync.remove(key).then(() => {
      console.log('清空一个值');
      asyncGetData()
    })
  } else {
    chrome.storage.sync.clear().then(() => {
      console.log('清空所有的值');
      document.getElementById("asyncDataBox").innerHTML = "数据全部清空了"
    })
  }
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
    // 显示Cookie
    showCookie()
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

function setCookie(url, key, val) {
  const cookieUrl = document.getElementById("cookieUrl").value
  let urlEdit = cookieUrl || url
  const configCookie = { "url": urlEdit, "name": key, "value": val }
  chrome.cookies.set(configCookie);
}