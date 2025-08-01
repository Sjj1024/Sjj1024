console.log('这是background脚本执行内容，浏览器启动或插件加载时运行');

chrome.action.setBadgeText({ text: "s" })

// 检测Cookie发生变化
chrome.cookies.onChanged.addListener((changeInfo) => {
  console.log('cookie发生变化了', changeInfo);
  var cause = changeInfo.cause
  var cookieKey = changeInfo.cookie.name
  var cookieDomain = "https://" + changeInfo.cookie.domain
  console.log('检测到cookie变化了', cookieKey, cause);
  if (cookieKey === "caoliuUserAgent" && cause === "overwrite") {
    console.log('检测到caoliuCookies的cookie变化了', changeInfo);
    chrome.action.setBadgeText({ text: "c" })
    // 获取所有的cookie值
    chrome.cookies.getAll({ "url": cookieDomain }, function (cookies) {
      console.log('得到的Cookie是：', cookies);
      // 拿到1024URl，userAgent，Cookies三个值
      var caoliuUrl = cookies.find(item => {
        if (item.name === "caoliuUrl")
          return item
      }).value.replaceAll("!!", ";")
      var caoliuUserAgent = cookies.find(item => {
        if (item.name === "caoliuUserAgent")
          return item
      }).value.replaceAll("!!", ";")
      var caoliuCookies = cookies.find(item => {
        if (item.name === "caoliuCookies")
          return item
      }).value.replaceAll("!!", ";").replaceAll("ismob=1", "ismob=0")
      console.log('得到的目标值是caoliuUrl:', caoliuUrl);
      console.log('得到的目标值是caoliuUserAgent:', caoliuUserAgent);
      console.log('得到的目标值是caoliuCookies:', caoliuCookies);
      // 设置目标站的cookie，并且设置userAgent
      chrome.action.setBadgeText({ text: "cao" })
      const cookieList = caoliuCookies.split(";")
      cookieList.forEach(item => {
        const keyVal = item.trim().split("=")
        setCookie(caoliuUrl, keyVal[0], keyVal[1])
      })
      console.log('Cookie修改成功');
      // 修改userAgent
      editUserAgent(caoliuUrl, caoliuUserAgent)
      chrome.action.setBadgeText({ text: "ua" })
      // 打开首页
      // var caoliuIndex = caoliuUrl + "/index.php"
      // chrome.tabs.create({ url: caoliuIndex });
    })
  }
  // 98
  if (cookieKey === "tangUserAgent" && cause) {
    console.log('检测到tangCookies的cookie变化了', changeInfo);
    chrome.action.setBadgeText({ text: "c" })
    // 获取所有的cookie值
    chrome.cookies.getAll({ "url": cookieDomain }, function (cookies) {
      console.log('得到的Cookie是：', cookies);
      // 拿到1024URl，userAgent，Cookies三个值
      var tangUrl = cookies.find(item => {
        if (item.name === "tangUrl")
          return item
      }).value.replaceAll("!!", ";")
      var tangUserAgent = cookies.find(item => {
        if (item.name === "tangUserAgent")
          return item
      }).value.replaceAll("!!", ";")
      var tangCookies = cookies.find(item => {
        if (item.name === "tangCookies")
          return item
      }).value.replaceAll("!!", ";").replaceAll("ismob=1", "ismob=0")
      console.log('得到的目标值是TangUrl:', tangUrl);
      console.log('得到的目标值是TangUserAgent:', tangUserAgent);
      console.log('得到的目标值是TangCookies:', tangCookies);
      // 设置目标站的cookie，并且设置userAgent
      chrome.action.setBadgeText({ text: "98" })
      const cookieList = tangCookies.split(";")
      cookieList.forEach(item => {
        const keyVal = item.trim().split("=")
        setCookie(tangUrl, keyVal[0], keyVal[1])
      })
      console.log('Cookie修改成功');
      // 修改userAgent
      editUserAgent(tangUrl, tangUserAgent)
      chrome.action.setBadgeText({ text: "ua" })
      // 打开首页
      // var caoliuIndex = caoliuUrl + "/index.php"
      // chrome.tabs.create({ url: caoliuIndex });
    })
  }
})


function setCookie(url, key, val) {
  if (url && key && val) {
    const configCookie = { "url": url, "name": key, "value": val }
    chrome.cookies.set(configCookie);
  } else {
    console.log('设置cookie出错了:', url, key, val);
  }
}


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

// 修改指定网站的userAgent，如果存在，先删除
function editUserAgent(url, userAgent) {
  var urlFilter = url.replaceAll("https://", "||")
  // 获取动态的规则getDynamicRules
  chrome.declarativeNetRequest.getDynamicRules(
    (rules) => {
      console.log('getDynamicRules-----', rules);
      // 如果存在id为2的规则，则先删除掉这个规则
      const rule = rules.find(item => item.id === 2)
      if (rule) {
        // 清除掉userAgent的rule
        console.log('发现了已存在的rule---', rule);
        delRules(2)
      }
      // 重新添加userAgent
      const rulesAdd = {
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
              urlFilter: urlFilter,
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
      addRules(rulesAdd)
    }
  )
}


// 消息传递
const user = {
  username: 'demo-user'
};

// 添加的规则内容
const configRules = [
  {
    id: 2,
    priority: 2,
    action: {
      type: 'modifyHeaders',
      requestHeaders: [
        {
          header: 'user-agent',
          operation: 'set',
          value: `Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25`,
        },
      ],
    },
    condition: {
      urlFilter: '|https*',
      resourceTypes: [
        'main_frame',
        'xmlhttprequest',
      ],
    },
  },
]

// 添加规则
async function addRules(rules) {
  // 更新动态规则的操作：添加、删除
  chrome.declarativeNetRequest.updateDynamicRules(rules, () => {
    if (chrome.runtime.lastError) {
      console.log('chrome.runtime.lastError-出错：', chrome.runtime.lastError);
    } else {
      console.log('添加请求头....addRules');
      chrome.declarativeNetRequest.getDynamicRules(rules => {
        console.log("addRules后的规则列表是:", rules)
      })
    }
  })
}

// 删除规则
async function delRules(ruleId) {
  console.log('删除ruleId', ruleId);
  const rulesDel = { removeRuleIds: [ruleId] }
  // 更新动态规则的操作：添加、删除
  chrome.declarativeNetRequest.updateDynamicRules(rulesDel, () => {
    if (chrome.runtime.lastError) {
      console.log('chrome.runtime.lastError-', chrome.runtime.lastError);
    } else {
      console.log('修改请求头.....delRules');
      chrome.declarativeNetRequest.getDynamicRules(rules => {
        console.log("delRules修改后的规则列表是:", rules)
      })
    }
  })
}

// 给content.js
async function sendContent(tabID) {
  const response = await chrome.tabs.sendMessage(tabID, { greeting: "hello" });
  // do something with response here, not outside the function
  console.log("sendContentResponse---", response);
}

// 添加规则
// const rules = {
//   addRules: [
//     {
//       id: 2,
//       priority: 2,
//       action: {
//         type: 'modifyHeaders',
//         requestHeaders: [
//           {
//             header: 'user-agent',
//             operation: 'set',
//             value: `Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25`,
//           },
//         ],
//       },
//       condition: {
//         urlFilter: '|https*',
//         resourceTypes: [
//           'main_frame',
//           'xmlhttprequest',
//         ],
//       },
//     },
//   ],
// }

// 移除规则
const rules = {
  removeRuleIds: [
    2
  ]
}

// 获取可用rules数量
// chrome.declarativeNetRequest.getAvailableStaticRuleCount(
//   (count) => {
//     console.log('StaticRuleCount----', count);
//   }
// )

// 获取动态的规则getDynamicRules
// chrome.declarativeNetRequest.getDynamicRules(
//   (rules) => {
//     console.log('getDynamicRules-----', rules);
//   }
// )

// 返回当前可用的静态规则id
// chrome.declarativeNetRequest.getEnabledRulesets(
//   (rulesetIds) => {
//     console.log('getEnabledRulesets---', rulesetIds);
//   }
// )

// getMatchedRules
// chrome.declarativeNetRequest.getMatchedRules(
//   (details) => {
//     console.log('getMatchedRules-----', details);
//   }
// )