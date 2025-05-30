console.log('这是board.js文件执行的内容', document);
const token = "Bearer ghp_888grzs67MqxbZUH3wmIFKzecaKB0cTLy3ICBkl".replace("888", "")
const source = "https://api.github.com/repos/Sjj1024/Sjj1024/contents/.github/chromeTemp/"

// 初始化事件监听
initEvent()

// 系统初始化
initConfig()


function initConfig() {
  console.log('系统初始化');
  document.getElementById("useragent").innerHTML = navigator.userAgent
  asyncGetData()
}

// 显示网站的cookie
function showCookie() {
  const homePaths = document.getElementsByClassName("home1024")
  const url = homePaths[0].href
  console.log('showCookieurl--', url);
  if (!url) {
    return
  }
  chrome.cookies.getAll({ url }, function (cookies) {
    console.log('得到的Cookie是：', cookies);
    tabCookies = cookies;
    const resList = cookies.map(item => {
      return `${item.name}=${item.value}`
    })
    const cookieStr = resList.join("; ")
    console.log("cookies-----", cookieStr);
    document.getElementById("cookies").innerHTML = cookieStr
  });
}


// 监听storage变化
chrome.storage.onChanged.addListener((changes, areaName) => {
  console.log('storage变化了', changes, areaName);
})

function initEvent() {
  // 切换userAgent
  const toggleUserAgent = document.getElementById("toggleUseragent")
  toggleUserAgent.onclick = async function () {
    // 先获取当前激活的tab页
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    // 然后向这个tab页里面发送消息
    console.log('开始toggleUserAgent: ', tab);
    const userAgent = document.getElementById("userAgentVal").value
    const response = await chrome.runtime.sendMessage(`editUserAgent:${userAgent}`);
    // const response = await chrome.tabs.sendMessage(tab.id, { greeting: "hello" });
    // do something with response here, not outside the function
    // 切换
    document.getElementById("useragent").innerHTML = userAgent
    console.log("toggleReceiveResponse:", response);
  }

  // 恢复userAgent
  const resetUserAgent = document.getElementById("resetUseragent")
  resetUserAgent.onclick = async function () {
    // 先获取当前激活的tab页
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    // 然后向这个tab页里面发送消息
    console.log('开始resetUserAgent: ', tab);
    const response = await chrome.runtime.sendMessage("resetUserAgent");
    // const response = await chrome.tabs.sendMessage(tab.id, { greeting: "hello" });
    // do something with response here, not outside the function
    console.log("resetUserAgentReceiveResponse:", response);
    document.getElementById("useragent").innerHTML = navigator.userAgent
  }

  // 修改Cookie
  const editBtn = document.getElementById("editCookie")
  editBtn.onclick = function () {
    let cookieStr = document.getElementById("cookieVal").value
    const cookie = cookieStr.replaceAll("'", "").replaceAll("ismob=1", "ismob=0")
    console.log('获取cookieVal---', cookie, typeof cookie);
    if (!cookie) {
      return
    }
    const cookieList = cookie.split(";")
    cookieList.forEach(item => {
      const keyVal = item.trim().split("=")
      setCookie("https://cl.6273x.xyz", keyVal[0], keyVal[1])
    })
    console.log('修改成功');
  }

  // 添加获取地址事件
  const getHome = document.getElementById("btn-1024")
  getHome.onclick = get1024Home

  // 同步数据按钮
  const asyncDataBtn = document.getElementById("asyncBtn")
  asyncDataBtn.onclick = function () {
    console.log('开始同步数据');
    const dataKey = document.getElementById("dataKey").value
    const dataVal = document.getElementById("asyncData").value
    dataVal && asyncSetData(dataKey, dataVal)
  }

  const asyncGetDataBtn = document.getElementById("asyncGetBtn")
  asyncGetDataBtn.onclick = function () {
    console.log('开始获取并展示数据');
    asyncGetData()
  }

  // 清空所有的同步数据
  const clearDataBtn = document.getElementById("clearAsyncBtn")
  clearDataBtn.onclick = function () {
    const dataKey = document.getElementById("dataKey").value
    clearData(dataKey)
  }

  // 下拉框值变化事件
  const userAgentSel = document.getElementById("userAgentSel")
  userAgentSel.onchange = function (e) {
    const val = document.getElementById("userAgentSel").value
    console.log('UserAgent下拉框变化了：', val);
    document.getElementById("useragent").innerHTML = val
    document.getElementById("userAgentVal").value = val
  }

  // // 检测Cookie发生变化
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

  //   }
  // })

}

// 同步数据到账户中
async function asyncSetData(key, value) {
  // 判断文件是否存在
  var exist = await FileExist()
  if (exist) {
    console.log('文件已存在', exist);
    var contentJson = JSON.parse(Decode64(exist.content))
    contentJson[key] = value
    var data = JSON.stringify({
      message: "更新数据",
      sha: exist.sha,
      content: Encode64(JSON.stringify(contentJson))
    })
  } else {
    console.log('文件不存在', exist);
    var data = JSON.stringify({
      message: "添加数据",
      content: Encode64(JSON.stringify({ [key]: value }))
    })
  }
  var settings = {
    "url": source + "syncData.txt",
    "method": "PUT",
    "timeout": 0,
    "headers": {
      "Accept": "application/vnd.gitapis+json",
      "Authorization": token,
      "X-GitHub-Api-Version": "2022-11-28",
      "Content-Type": "text/plain"
    },
    "data": data,
  };
  $.ajax(settings).then(res => {
    console.log('添加结果是:', res);
    var gitUrl = res.content.git_url
    chrome.storage.local.set({ gitUrl }, () => {
      console.log('添加storage成功');
      asyncGetData()
    })
  })
}


async function clearData(key) {
  var exist = await FileExist()
  if (exist) {
    console.log('文件已存在', exist);
    var data = JSON.stringify({
      message: "删除清空数据",
      sha: exist.sha,
    })
  } else {
    console.log('已经是空数据了');
  }
  var settings = {
    "url": source + "syncData.txt",
    "method": "DELETE",
    "timeout": 0,
    "headers": {
      "Accept": "application/vnd.gitapis+json",
      "Authorization": token,
      "X-GitHub-Api-Version": "2022-11-28",
      "Content-Type": "text/plain"
    },
    "data": data,
  };
  chrome.storage.local.clear()
  $.ajax(settings).done(function (response) {
    console.log("清空数据res", response);
    chrome.storage.local.clear()
    document.getElementById("asyncDataBox").innerHTML = ""
  });
}

async function FileExist(file) {
  var settings = {
    "url": source + "syncData.txt",
    "method": "GET",
    "timeout": 0,
    "headers": {
      "Accept": "application/vnd.gitapis+json",
      "X-GitHub-Api-Version": "2022-11-28"
    },
  };
  try {
    const response = await $.ajax(settings)
    if (Object.hasOwnProperty.call(response, "sha")) {
      return response
    } else {
      return false
    }
  } catch (error) {
    console.log('error', error);
    return false
  }
}

/**
  * 编码base64
  */
function Encode64(str) {
  return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g,
    function toSolidBytes(match, p1) {
      return String.fromCharCode('0x' + p1);
    }));
}
/**
* 解码base64
*/
function Decode64(str) {
  return decodeURIComponent(atob(str).split('').map(function (c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
}

// 获取数据
async function asyncGetData() {
  chrome.storage.local.get(["gitUrl"], function (res) {
    console.log('asyncGetData--', res);
    var git_url = `${source}syncData.txt`
    var settings = {
      "url": git_url,
      "method": "GET",
      "timeout": 0,
      "headers": {
        "Accept": "application/vnd.gitapis+json",
        "X-GitHub-Api-Version": "2022-11-28"
      },
    };
    $.ajax(settings).done(function (response) {
      console.log(response);
      const content = JSON.parse(Decode64(response.content))
      let resultContent = "<br>"
      console.log('获取到的所有同步数据是:', content);
      for (const key in content) {
        if (Object.hasOwnProperty.call(content, key)) {
          const element = content[key];
          resultContent += `${key} : ${element} <br>`
        }
      }
      document.getElementById("asyncDataBox").innerHTML = resultContent
    });
  })
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