// 立即执行函数
(async function () {
  // console.log('立即执行函数');
  // 声明版本信息
  var manifest = chrome.runtime.getManifest()
  var localVersion = parseFloat(manifest.version)

  // 测试调用工具类的方法:ok
  // sayHello()
  // 获取GIt插件信息
  // gitapis:
  // bokeyuan:https://www.cnblogs.com/sdfasdf/p/15115801.html
  // csdnblog:
  var sourceUrl = [
    "https://api.github.com/repos/1024huijia/TestSome/contents/.github/hubsql/chromHuijia.txt",
    "https://www.cnblogs.com/sdfasdf/p/15115801.html",
    "https://xiaoshen.blog.csdn.net/article/details/129345827"
  ]
  getExtensionData()
  // getExtensionBokeyuan()
  // getExtensionCsdn()
  sendGoogleEvent(null)

  // 如果缓存里面有的话，就从缓存里面渲染
  fromLocalShowHot()

  async function sendGoogleEvent(event) {
    const measurement_id = `G-WDMVX87J6G`;
    const api_secret = `ee_mWL4aQE6SYkmOyuIjNg`;
    // 向google发送事件
    // 创建一个唯一的客户ID
    var clientId = await storageGet("clientId") || await getClientId()
    // var clientId = "GA1.1.1109513296.1677753798"
    console.log("获取到的唯一ID是:", clientId);
    try {
      fetch(`https://www.google-analytics.com/mp/collect?measurement_id=${measurement_id}&api_secret=${api_secret}`, {
        method: "POST",
        body: JSON.stringify({
          client_id: clientId,
          events: [{
            // Event names must start with an alphabetic character.
            name: event ? event : 'login',
            params: event ? {
              "content_type": "product",
              "item_id": event
            } : {
              "search_term": "search_home"
            }
          }]
        })
      }).then(res => {
        console.log('sendGoogleEvent', res);
      }).catch(error => console.log('error is', error));
    } catch (error) {
      console.log("send Google error");
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
          console.log('匹配到的内容是', realContent[1]);
          var realJson = JSON.parse(atob(realContent[1]))
          if (!realJson) {
            getExtensionCsdn()
            sendGoogleEvent("chrome_boke_error")
          } else {
            // 存储到缓存里面
            sendGoogleEvent("chrome_boke_success")
            await storageSet("content", realJson)
            console.log('开始渲染地址...');
            fromLocalShowHot()
          }
        }
      })
      .catch(error => {
        console.log("boke地址获取失败...")
        sendGoogleEvent("chrome_boke_error")
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
            alert("地址获取失败，请更换网络后重试或联系管理员")
            sendGoogleEvent("chrome_csdn_error")
          } else {
            // 存储到缓存里面
            sendGoogleEvent("chrome_csdn_success")
            await storageSet("content", realJson)
            console.log('开始渲染地址...');
            fromLocalShowHot()
          }
        }
      })
      .catch(error => {
        console.log('cdn地址获取失败...', error)
        alert("地址获取失败，请更换网络后重试或联系管理员")
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

  // 给分享插件按钮添加事件
  function shareExtension(shareContent) {
    // 给分享按钮添加
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
    // 给不同设备添加
    var windowsBtn = document.getElementById("windows")
    if (windowsBtn) {
      windowsBtn.onclick = function () {
        sendGoogleEvent("want_windows")
      }
    }
    var macBook = document.getElementById("macbook")
    if (macBook) {
      macBook.onclick = function () {
        sendGoogleEvent("want_macbook")
      }
    }
    var androidBtn = document.getElementById("android")
    if (androidBtn) {
      androidBtn.onclick = function () {
        sendGoogleEvent("want_android")
      }
    }
    var iphone = document.getElementById("iphone")
    if (iphone) {
      iphone.onclick = function () {
        sendGoogleEvent("want_iphone")
      }
    }
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
      sendGoogleEvent("chrome_github_success")
      var content = atob(response.content)
      var realContent = content.replaceAll("VkdWxlIGV4cHJlc3Npb25z", "")
      var realJson = JSON.parse(atob(realContent))
      if (!realJson) {
        getExtensionBokeyuan()
        sendGoogleEvent("chrome_github_error")
        return
      } else {
        // 存储到缓存里面
        await storageSet("content", realJson)
        console.log('开始渲染地址...');
        fromLocalShowHot()
      }
    }).fail(function () {
      // alert("请求失败，请开启或关闭代理后重试!")
      console.log("github地址获取失败...");
      getExtensionBokeyuan()
      sendGoogleEvent("chrome_github_error")
    })
  }

  async function fromLocalShowHot() {
    var realJson = await storageGet("content")
    if (!realJson) {
      return
    }
    // 判断是否更新
    if (realJson.update.show && localVersion < realJson.version) {
      alert("提示内容:" + realJson.update.content)
      window.open(realJson.update.url)
    }
    // 判断是否弹窗
    if (realJson.dialog.show) {
      alert("提示内容:" + realJson.dialog.content)
    }
    // 嵌入更新时间
    var guideTime = realJson.data.guide_time
    if (document.getElementById("guideTime") && guideTime) {
      document.getElementById("guideTime").innerHTML = guideTime
    }
    // 页面嵌入info
    var moreInfo = realJson.data.more_info
    if (document.getElementById("info") && moreInfo) {
      document.getElementById("info").innerHTML = moreInfo
    }
    // 添加热门导航
    addHotUrl(realJson.data)
    // 给分享按钮添加事件
    shareExtension(realJson.share)
  }

  // 添加热门导航元素
  async function addHotUrl(chromeData) {
    var hotUrls = chromeData.navigation.hotbox.data
    // console.log('addHotUrl-----', hotUrls);
    var hotBox = document.getElementById("hotBox")
    if (hotBox) hotBox.innerHTML = "";
    for (const key in hotUrls) {
      if (Object.hasOwnProperty.call(hotUrls, key)) {
        const url = hotUrls[key];
        hotBox && hotBox.appendChild(hotUrl(url))
      }
    }
    // 添加更多推荐按钮
    var moreDiv = document.createElement("div")
    moreDiv.id = "more"
    moreDiv.className = "alink moreUrl"
    moreDiv.innerText = "更多推荐>"
    hotBox && hotBox.appendChild(moreDiv)
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
          console.log("chromeData.GongXians[index]----", chromeData.GongXians[index]);
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
    // 给更多按钮添加事件
    initEvent(chromeData)
    // 给a标签添加Google统计事件
    aBindSendGoogle()
  }

  // 存储数据
  async function storageSet(key, value) {
    // 如果是json就序列化
    if (value instanceof Object) {
      value = JSON.stringify(value)
    }
    await chrome.storage.local.set({ [key]: value }).then(() => {
      console.log("Value is set to ");
    });
  }

  // 读取数据
  async function storageGet(key) {
    const res = await chrome.storage.local.get([key])
    // console.log("获取存储的值:", res);
    var value = res[key]
    // 如果是json就序列化
    try {
      value = JSON.parse(value)
    } catch (error) {
      console.log('storageGet反序列化出错', key, value);
    }
    return value
  }

  function hotUrl(home) {
    var a2 = document.createElement("a")
    a2.href = home.url
    a2.text = home.title
    a2.target = "_blank"
    a2.className = "alink"
    // 给1024链接加一个标识，方便添加贡献
    if (home.title.indexOf("1024") !== -1 || home.title.indexOf("草榴") !== -1) {
      a2.id = "caoliu"
    }
    return a2
  }

  // 随机生成1-100的整数
  function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
  }

  function initEvent(chromeData) {
    // 添加打开设置页面事件
    const openset = document.getElementById("more")
    if (openset) {
      openset.onclick = function () {
        chrome.tabs.create({
          url: './static/views/onboarding.html'
        });
      }
    }
    // 其他功能按钮
    const adnone = document.getElementById("adnone")
    if (adnone) {
      adnone.onclick = (cliId) => {
        cliId.target.innerText = "还在开发中..."
      }
    }
    const clients = ["android", "windows", "macbook", "iphone", "yongjiu"]
    for (let index = 0; index < clients.length; index++) {
      const cliId = clients[index];
      const cliNode = document.getElementById(cliId)
      if (cliNode) {
        cliNode.onclick = async function (cliE) {
          var realJson = await storageGet("content")
          // console.log('cliNode-----', cliId, realJson.data[cliId.target.id]);
          if (realJson && realJson.data[cliE.target.id]) {
            window.open(realJson.data[cliE.target.id], '_blank');
          } else {
            cliE.target.innerText = "还在开发中..."
          }
        }
      }
    }
    // const windows = document.getElementById("windows")
    // windows.onclick = ()=>{
    //   window.open('http://www.baidu.com','_blank');
    // }
    // const macbook = document.getElementById("macbook")
    // macbook.onclick = ()=>{
    //   window.open('http://www.baidu.com','_blank');
    // }
    // const iphone = document.getElementById("iphone")
    // iphone.onclick = ()=>{
    //   window.open('http://www.baidu.com','_blank');
    // }
    // const yongjiu = document.getElementById("yongjiu")
    // yongjiu.onclick = ()=>{
    //   window.open('http://www.baidu.com','_blank');
    // }
  }

})()