console.log('这是内容脚本执行的');

// 选中csdn的调研卡片隐藏:类似于去除广告
window.onload = function () {
  const npsBox = document.getElementById("nps-box")
  console.log('npsBox----', npsBox);
  if (npsBox) {
    setTimeout(() => {
      npsBox.style.display = "none"
      console.log('修改完成');
      document.getElementById("nps-box").style.display = "none"
    }, 1000);
  }


  // 监听storage变化
  // var dumpIndex = document.getElementById("dumpIndex")
  // if (dumpIndex) {
  //   dumpIndex.onclick = function () {
  //     console.log('按钮被点击了');
  //   }
  // }

  // 修改网站标题等内容
  // const biadufanyi = document.getElementsByClassName("navigation-text")
  // const biadufanyi = document.getElementsByTagName('b')
  // console.log('百度翻译列表-----', biadufanyi);
  // for (let index = 0; index < biadufanyi.length; index++) {
  //   const element = biadufanyi[index];
  //   // console.log('elementText---',element.innerText);
  //   if (element.innerText === "草榴社區") {
  //     console.log('找到了草榴社區');
  //     element.innerText = "HTML社区"
  //   } else {
  //     console.log('没有找到视频翻译');
  //   }
  // }
}

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

// 98堂一键评分
function postPingFen(){
  console.log("一件评分送上---");
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