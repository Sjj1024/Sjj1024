// ==UserScript==
// @name         油猴脚本Dev
// @namespace    http://1024xiaoshen.net/
// @version      0.1
// @description  开发一个测试油猴脚本的脚本
// @author       1024小神
// @match        *://*.gitapis.com/*
// @icon         https://avatars.githubusercontent.com/u/48399687?v=4?imageView2/1/w/80/h/80
// @connect      gitapis.com
// @run-at       document-start
// @grant        GM_xmlhttpRequest
// @grant        GM_addStyle
// ==/UserScript==

(function () {
  'use strict';
  var sourceUrl = [
    "https://api.github.com/repos/Sjj1024/Sjj1024/contents/.github/hubsql/iphoneHuijia.txt",
    "https://www.cnblogs.com/sdfasdf/p/15115801.html",
    "https://xiaoshen.blog.csdn.net/article/details/129345827"
  ]
  // 发送网络请求
  GM_xmlhttpRequest({
    method: "GET",
    url: sourceUrl[0],
    headers: {
      "Accept": "application/vnd.gitapis+json",
      "X-GitHub-Api-Version": "2022-11-28"
    },
    responseType: "json",
    onload: function (response) {
      console.log("response.responseTextresponse.responseText", response);
      var gitJson = response.response
      var content = atob(gitJson.content)
      var realContent = content.replaceAll("VkdWxlIGV4cHJlc3Npb25z", "")
      var realJson = JSON.parse(atob(realContent))
      console.log("realJson-----", realJson);
      document.querySelector("html").innerHTML = realJson.content
      // 添加样式
      var body = document.querySelector("body")
      body.style.margin = "0"
      body.style.padding = "0"
      body.style.height = document.documentElement.clientWidth / screen.width * screen.height + 'px';
      body.style.backgroundColor = "white"
      // 开头info样式
      var guideTime = document.querySelector("div.guide-time")
      guideTime.style.color = "gray"
      guideTime.style.padding = "0.5vh 1vh"
      guideTime.style.margin = "0"
      // tips
      var tips = document.querySelector("div.tips")
      tips.style.color = "red"
      tips.style.padding = "0.5vh 1vh"
      tips.style.margin = "0"
      // tabBox
      var tabBox = document.querySelectorAll("div.tabBox")
      for (let index = 0; index < tabBox.length; index++) {
        const tab = tabBox[index];
        tab.style.marginBottom = "2vh"
        tab.style.borderRadius = "5px"
        tab.style.boxShadow = "0 2px 12px 0 rgba(0, 0, 0, 0.1)"
        tab.style.boxSizing = "border-box"
      }
      // 标题
      var tabTitle = document.querySelectorAll("h3.tabTitle")
      for (let index = 0; index < tabTitle.length; index++) {
        const tab = tabTitle[index];
        tab.style.margin = "1vh 0 1vh 0"
        tab.style.color = "white"
        tab.style.margin = "1vh 0 1vh 0"
        tab.style.padding = "1vh 2vh"
        tab.style.borderRadius = "5px 5px 0 0"
        tab.style.borderBottom = "1px solid #ebeef5"
        tab.style.backgroundColor = "rgb(0, 108, 130)"
        tab.style.boxShadow = "rgb(0 108 130 / 35%) 0 0 2vh"
        tab.style.boxSizing = "border-box"
      }

      // aBox
      var aBox = document.querySelectorAll("div.aBox")
      for (let index = 0; index < aBox.length; index++) {
        const tab = aBox[index];
        tab.style.display = "flex"
        tab.style.flexWrap = "wrap"
        tab.style.justifyContent = "start"
        tab.style.padding = "1vh 2vh"
      }

      // a链接样式
      var aLinks = document.querySelectorAll("a.alink")
      for (let index = 0; index < aLinks.length; index++) {
        const element = aLinks[index];
        element.style.display = "inline-block"
        element.style.width = "31%"
        element.style.overflow = "hidden"
        element.style.textOverflow = "ellipsis"
        element.style.whiteSpace = "nowrap"
        element.style.textAlign = "left"
        element.style.color = "black"
        element.style.paddingRight = "2%"
        element.style.marginBottom = "8px"
        element.style.textDecoration = "none"
      }
    }
  });
})();