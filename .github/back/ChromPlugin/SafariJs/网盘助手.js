// ==UserScript==
// @name         网盘助手
// @namespace    http://go.newday.me/s/pan-home
// @version      0.4.8
// @icon         http://cdn.newday.me/addon/pan/favicon.ico
// @author       哩呵
// @description  一个优雅好用的网盘助手；插件主要功能有：[1]记住各大网盘分享的访问密钥 [2]百度网盘生成并展示下载链接 [3]百度网盘分享时自定义提取码
// @match        *://pan.baidu.com/*
// @match        *://yun.baidu.com/*
// @match        *://*.weiyun.com/*
// @match        *://*.lanzous.com/*
// @match        *://*.lanzoux.com/*
// @match        *://cloud.189.cn/*
// @match        *://*.newday.me/*
// @match        *://*.likestyle.cn/*
// @connect      newday.me
// @connect      likestyle.cn
// @require      https://cdn.staticfile.org/jquery/3.5.0/jquery.min.js
// @require      https://cdn.staticfile.org/dompurify/2.0.10/purify.min.js
// @require      https://cdn.staticfile.org/snap.svg/0.5.1/snap.svg-min.js
// @run-at       document-start
// @grant        unsafeWindow
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_deleteValue
// @grant        GM_listValues
// @grant        GM_openInTab
// @grant        GM_notification
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function () {
  'use strict';

  var manifest = {
      "name": "wpzs",
      "title": "网盘助手",
      "urls": {},
      "apis": {
          "version": "https://api.newday.me/share/disk/version",
          "origin": "https://api.newday.me/share/disk/origin"
      },
      "logger_level": 3,
      "options_page": "http://go.newday.me/s/pan-option"
  };

  var container = (function () {
      var obj = {
          defines: {},
          modules: {}
      };

      obj.define = function (name, requires, callback) {
          name = obj.processName(name);
          obj.defines[name] = {
              requires: requires,
              callback: callback
          };
      };

      obj.require = function (name, cache) {
          if (typeof cache == "undefined") {
              cache = true;
          }

          name = obj.processName(name);
          if (cache && obj.modules.hasOwnProperty(name)) {
              return obj.modules[name];
          } else if (obj.defines.hasOwnProperty(name)) {
              var requires = obj.defines[name].requires;
              var callback = obj.defines[name].callback;

              var module = obj.use(requires, callback);
              cache && obj.register(name, module);
              return module;
          }
      };

      obj.use = function (requires, callback) {
          var module = {
              exports: undefined
          };
          var params = obj.buildParams(requires, module);
          var result = callback.apply(this, params);
          if (typeof result != "undefined") {
              return result;
          } else {
              return module.exports;
          }
      };

      obj.register = function (name, module) {
          name = obj.processName(name);
          obj.modules[name] = module;
      };

      obj.buildParams = function (requires, module) {
          var params = [];
          requires.forEach(function (name) {
              params.push(obj.require(name));
          });
          params.push(obj.require);
          params.push(module.exports);
          params.push(module);
          return params;
      };

      obj.processName = function (name) {
          return name.toLowerCase();
      };

      return {
          define: obj.define,
          use: obj.use,
          register: obj.register,
          modules: obj.modules
      };
  })();

  container.define("gm", [], function () {
      var obj = {};

      obj.ready = function (callback) {
          if (typeof GM_getValue != "undefined") {
              callback && callback();
          }
          else {
              setTimeout(function () {
                  obj.ready(callback);
              }, 100);
          }
      };

      return obj;
  });

  /** common **/
  container.define("gmDao", [], function () {
      var obj = {
          items: {}
      };

      obj.get = function (name) {
          return GM_getValue(name);
      };

      obj.getBatch = function (names) {
          var items = {};
          names.forEach(function (name) {
              items[name] = obj.get(name);
          });
          return items;
      };

      obj.getAll = function () {
          return obj.getBatch(GM_listValues());
      };

      obj.set = function (name, item) {
          GM_setValue(name, item);
      };

      obj.setBatch = function (items) {
          for (var name in items) {
              obj.set(name, items[name]);
          }
      };

      obj.setAll = function (items) {
          var names = GM_listValues();
          names.forEach(function (name) {
              if (!items.hasOwnProperty(name)) {
                  obj.remove(name);
              }
          });
          obj.setBatch(items);
      };

      obj.remove = function (name) {
          GM_deleteValue(name);
      };

      obj.removeBatch = function (names) {
          names.forEach(function (name) {
              obj.remove(name);
          });
      };

      obj.removeAll = function () {
          obj.removeBatch(GM_listValues());
      };

      return obj;
  });

  container.define("ScopeDao", [], function () {
      return function (dao, scope) {
          var obj = {
              items: {}
          };

          obj.get = function (name) {
              return obj.items[name];
          };

          obj.getBatch = function (names) {
              var items = {};
              names.forEach(function (name) {
                  if (obj.items.hasOwnProperty(name)) {
                      items[name] = obj.items[name];
                  }
              });
              return items;
          };

          obj.getAll = function () {
              return obj.items;
          };

          obj.set = function (name, item) {
              obj.items[name] = item;

              obj.sync();
          };

          obj.setBatch = function (items) {
              obj.items = Object.assign(obj.items, items);

              obj.sync();
          };

          obj.setAll = function (items) {
              obj.items = Object.assign({}, items);

              obj.sync();
          };

          obj.remove = function (name) {
              delete obj.items[name];

              obj.sync();
          };

          obj.removeBatch = function (names) {
              names.forEach(function (name) {
                  delete obj.items[name];
              });

              obj.sync();
          };

          obj.removeAll = function () {
              obj.items = {};

              obj.getDao().remove(obj.getScope());
          };

          obj.init = function () {
              var items = obj.getDao().get(obj.getScope());
              if (items instanceof Object) {
                  obj.items = items;
              }
          };

          obj.sync = function () {
              obj.getDao().set(obj.getScope(), obj.items);
          };

          obj.getDao = function () {
              return dao;
          };

          obj.getScope = function () {
              return scope;
          };

          return obj.init(), obj;
      };
  });

  container.define("config", ["factory"], function (factory) {
      var obj = {};

      obj.getConfig = function (name) {
          return obj.getDao().get(name);
      };

      obj.setConfig = function (name, value) {
          obj.getDao().set(name, value);
      };

      obj.delConfig = function (name) {
          obj.getDao().remove(name);
      };

      obj.getAll = function () {
          return obj.getDao().getAll();
      };

      obj.getDao = function () {
          return factory.getConfigDao();
      };

      return obj;
  });

  container.define("storage", ["factory"], function (factory) {
      var obj = {};

      obj.getValue = function (name) {
          return obj.getDao().get(name);
      };

      obj.setValue = function (name, value) {
          obj.getDao().set(name, value);
      };

      obj.getAll = function () {
          return obj.getDao().getAll();
      };

      obj.getDao = function () {
          return factory.getStorageDao();
      };

      return obj;
  });

  container.define("option", ["config", "constant"], function (config, constant) {
      var obj = {
          name: "option",
          constant: constant.option
      };

      obj.isOptionActive = function (item) {
          var name = item.name;
          var option = obj.getOption();
          return option.indexOf(name) >= 0 ? true : false;
      };

      obj.setOptionActive = function (item) {
          var name = item.name;
          var option = obj.getOption();
          if (option.indexOf(name) < 0) {
              option.push(name);
              obj.setOption(option);
          }
      };

      obj.setOptionUnActive = function (item) {
          var name = item.name;
          var option = obj.getOption();
          var index = option.indexOf(name);
          if (index >= 0) {
              delete option[index];
              obj.setOption(option);
          }
      };

      obj.getOption = function () {
          var option = [];
          var optionList = obj.getOptionList();
          Object.values(obj.constant).forEach(function (item) {
              var name = item.name;
              if (optionList.hasOwnProperty(name)) {
                  if (optionList[name] != "no") {
                      option.push(name);
                  }
              }
              else if (item.value != "no") {
                  option.push(name);
              }
          });
          return option;
      };

      obj.setOption = function (option) {
          var optionList = {};
          Object.values(obj.constant).forEach(function (item) {
              var name = item.name;
              if (option.indexOf(name) >= 0) {
                  optionList[name] = "yes";
              } else {
                  optionList[name] = "no";
              }
          });
          obj.setOptionList(optionList);
      };

      obj.getOptionList = function () {
          var optionList = config.getConfig(obj.name);
          return optionList ? optionList : {};
      };

      obj.setOptionList = function (optionList) {
          config.setConfig(obj.name, optionList);
      };

      return obj;
  });

  container.define("manifest", [], function () {
      var obj = {
          manifest: manifest
      };

      obj.getItem = function (name) {
          return obj.manifest[name];
      };

      obj.getManifest = function () {
          return obj.manifest;
      };

      obj.getName = function () {
          return obj.getItem("name");
      };

      obj.getTitle = function () {
          return obj.getItem("title");
      };

      obj.getUrl = function (name) {
          var urls = obj.getItem("urls");
          (urls instanceof Object) || (urls = {});
          return urls[name];
      };

      obj.getApi = function (name) {
          var apis = obj.getItem("apis");
          (apis instanceof Object) || (apis = {});
          return apis[name];
      };

      obj.getOptionsPage = function () {
          if (GM_info.script.optionUrl) {
              return GM_info.script.optionUrl;
          }
          else {
              return obj.getItem("options_page");
          }
      };

      return obj;
  });

  container.define("env", ["config", "manifest"], function (config, manifest) {
      var obj = {
          modes: {
              ADDON: "addon",
              SCRIPT: "script"
          },
          browsers: {
              FIREFOX: "firefox",
              EDG: "edg",
              EDGE: "edge",
              BAIDU: "baidu",
              LIEBAO: "liebao",
              UC: "uc",
              QQ: "qq",
              SOGOU: "sogou",
              OPERA: "opera",
              MAXTHON: "maxthon",
              IE2345: "2345",
              SE360: "360",
              CHROME: "chrome",
              SAFIRI: "safari",
              OTHER: "other"
          }
      };

      obj.getName = function () {
          return manifest.getName();
      };

      obj.getMode = function () {
          if (GM_info.mode) {
              return GM_info.mode;
          }
          else {
              return obj.modes.SCRIPT;
          }
      };

      obj.getAid = function () {
          if (GM_info.scriptHandler) {
              return GM_info.scriptHandler.toLowerCase();
          }
          else {
              return "unknown";
          }
      };

      obj.getUid = function () {
          var uid = config.getConfig("uid");
          if (!uid) {
              uid = obj.randString(32);
              config.setConfig("uid", uid);
          }
          return uid;
      };

      obj.getBrowser = function () {
          if (!obj._browser) {
              obj._browser = obj.matchBrowserType(navigator.userAgent);
          }
          return obj._browser;
      };

      obj.getVersion = function () {
          return GM_info.script.version;
      };

      obj.getEdition = function () {
          return GM_info.version;
      };

      obj.getInfo = function () {
          return {
              mode: obj.getMode(),
              aid: obj.getAid(),
              uid: obj.getUid(),
              browser: obj.getBrowser(),
              version: obj.getVersion(),
              edition: obj.getEdition()
          };
      };

      obj.matchBrowserType = function (userAgent) {
          var browser = obj.browsers.OTHER;
          userAgent = userAgent.toLowerCase();
          if (userAgent.match(/firefox/) != null) {
              browser = obj.browsers.FIREFOX;
          } else if (userAgent.match(/edge/) != null) {
              browser = obj.browsers.EDGE;
          } else if (userAgent.match(/edg/) != null) {
              browser = obj.browsers.EDG;
          } else if (userAgent.match(/bidubrowser/) != null) {
              browser = obj.browsers.BAIDU;
          } else if (userAgent.match(/lbbrowser/) != null) {
              browser = obj.browsers.LIEBAO;
          } else if (userAgent.match(/ubrowser/) != null) {
              browser = obj.browsers.UC;
          } else if (userAgent.match(/qqbrowse/) != null) {
              browser = obj.browsers.QQ;
          } else if (userAgent.match(/metasr/) != null) {
              browser = obj.browsers.SOGOU;
          } else if (userAgent.match(/opr/) != null) {
              browser = obj.browsers.OPERA;
          } else if (userAgent.match(/maxthon/) != null) {
              browser = obj.browsers.MAXTHON;
          } else if (userAgent.match(/2345explorer/) != null) {
              browser = obj.browsers.IE2345;
          } else if (userAgent.match(/chrome/) != null) {
              if (navigator.mimeTypes.length > 10) {
                  browser = obj.browsers.SE360;
              } else {
                  browser = obj.browsers.CHROME;
              }
          } else if (userAgent.match(/safari/) != null) {
              browser = obj.browsers.SAFIRI;
          }
          return browser;
      };

      obj.randString = function (length) {
          var possible = "abcdefghijklmnopqrstuvwxyz0123456789";
          var text = "";
          for (var i = 0; i < length; i++) {
              text += possible.charAt(Math.floor(Math.random() * possible.length));
          }
          return text;
      };

      return obj;
  });

  container.define("http", [], function () {
      var obj = {};

      obj.ajax = function (option) {
          var details = {
              method: option.type,
              url: option.url,
              responseType: option.dataType,
              onload: function (result) {
                  if (!result.status || parseInt(result.status / 100) == 2) {
                      option.success && option.success(result.response);
                  }
                  else {
                      option.error && option.error("");
                  }
              },
              onerror: function (result) {
                  option.error && option.error(result.error);
              }
          };

          // 提交数据
          if (option.data instanceof Object) {
              if (option.data instanceof FormData) {
                  details.data = option.data;
              }
              else {
                  var formData = new FormData();
                  for (var i in option.data) {
                      formData.append(i, option.data[i]);
                  }
                  details.data = formData;
              }
          }

          // 自定义头
          if (option.headers) {
              details.headers = option.headers;
          }

          // 超时
          if (option.timeout) {
              details.timeout = option.timeout;
          }

          GM_xmlhttpRequest(details);
      };

      return obj;
  });

  container.define("router", [], function () {
      var obj = {};

      obj.getUrl = function () {
          return location.href;
      };

      obj.goUrl = function (url) {
          location.href = url;
      };

      obj.openUrl = function (url) {
          window.open(url);
      };

      obj.openTab = function (url, active) {
          GM_openInTab(url, !active);
      };

      obj.jumpLink = function (jumpUrl, jumpMode) {
          switch (jumpMode) {
              case 9:
                  // self
                  obj.goUrl(jumpUrl);
                  break;
              case 6:
                  // new
                  obj.openUrl(jumpUrl);
                  break;
              case 3:
                  // new & not active
                  obj.openTab(jumpUrl, false);
                  break;
              case 1:
                  // new & active
                  obj.openTab(jumpUrl, true);
                  break;
          }
      };

      obj.getUrlParam = function (name) {
          var param = obj.parseUrlParam(obj.getUrl());
          if (name) {
              return param.hasOwnProperty(name) ? param[name] : null;
          }
          else {
              return param;
          }
      };

      obj.parseUrlParam = function (url) {
          if (url.indexOf("?")) {
              url = url.split("?")[1];
          }
          var reg = /([^=&\s]+)[=\s]*([^=&\s]*)/g;
          var obj = {};
          while (reg.exec(url)) {
              obj[RegExp.$1] = RegExp.$2;
          }
          return obj;
      };

      return obj;
  });

  container.define("logger", ["env", "manifest"], function (env, manifest) {
      var obj = {
          constant: {
              DEBUG: 0,
              INFO: 1,
              WARN: 2,
              ERROR: 3,
              NONE: 4
          }
      };

      obj.debug = function (message) {
          obj.log(message, obj.constant.DEBUG);
      };

      obj.info = function (message) {
          obj.log(message, obj.constant.INFO);
      };

      obj.warn = function (message) {
          obj.log(message, obj.constant.WARN);
      };

      obj.error = function (message) {
          obj.log(message, obj.constant.ERROR);
      };

      obj.log = function (message, level) {
          if (level < manifest.getItem("logger_level")) {
              return false;
          }

          console.group("[" + env.getName() + "]" + env.getMode());
          console.log(message);
          console.groupEnd();
      };

      return obj;
  });

  container.define("meta", ["env", "$"], function (env, $) {
      var obj = {};

      obj.existMeta = function (name) {
          name = obj.processName(name);
          if ($("meta[name='" + name + "']").length) {
              return true;
          }
          else {
              return false;
          }
      };

      obj.appendMeta = function (name, content) {
          name = obj.processName(name);
          content || (content = "on");
          $('<meta name="' + name + '" content="on">').appendTo($("head"));
      };

      obj.processName = function (name) {
          return env.getName() + "::" + name;
      };

      return obj;
  });

  container.define("unsafeWindow", [], function () {
      if (typeof unsafeWindow == "undefined") {
          return window;
      }
      else {
          return unsafeWindow;
      }
  });

  container.define("svgCrypt", ["Snap"], function (Snap) {
      var obj = {};

      obj.getReqData = function () {
          var reqTime = Math.round(new Date().getTime() / 1000);
          var reqPoint = obj.getStrPoint("timestamp:" + reqTime);
          return {
              req_time: reqTime,
              req_point: reqPoint
          };
      };

      obj.getStrPoint = function (str) {
          if (str.length < 2) {
              return "0:0";
          }

          var path = "";
          var current, last = str[0].charCodeAt();
          var sum = last;
          for (var i = 1; i < str.length; i++) {
              current = str[i].charCodeAt();
              if (i == 1) {
                  path = path + "M";
              } else {
                  path = path + " L";
              }
              path = path + current + " " + last;
              last = current;
              sum = sum + current;
          }
          path = path + " Z";
          var index = sum % str.length;
          var data = Snap.path.getPointAtLength(path, str[index].charCodeAt());
          return data.m.x + ":" + data.n.y;
      };

      return obj;
  });

  container.define("calendar", [], function () {
      var obj = {};

      obj.getTime = function () {
          return (new Date()).getTime();
      };

      obj.formatTime = function (format, timestamp) {
          format || (format = "Y-m-d H:i:s");
          timestamp || (timestamp = obj.getTime());
          var date = new Date(timestamp);
          var year = 1900 + date.getYear();
          var month = "0" + (date.getMonth() + 1);
          var day = "0" + date.getDate();
          var hour = "0" + date.getHours();
          var minute = "0" + date.getMinutes();
          var second = "0" + date.getSeconds();
          var vars = {
              "Y": year,
              "m": month.substring(month.length - 2, month.length),
              "d": day.substring(day.length - 2, day.length),
              "H": hour.substring(hour.length - 2, hour.length),
              "i": minute.substring(minute.length - 2, minute.length),
              "s": second.substring(second.length - 2, second.length)
          };
          return obj.replaceVars(vars, format);
      };

      obj.replaceVars = function (vars, value) {
          Object.keys(vars).forEach(function (key) {
              value = value.replace(key, vars[key]);
          });
          return value;
      };

      return obj;
  });

  container.define("oneData", ["env", "http", "setting"], function (env, http, setting) {
      var obj = {};

      obj.requestOneApi = function (url, data, callback) {
          http.ajax({
              type: "post",
              url: url,
              dataType: "json",
              data: Object.assign(env.getInfo(), data, { access_token: setting.getAccessToken() }),
              success: function (response) {
                  callback && callback(response);
              },
              error: function () {
                  callback && callback("");
              }
          });
      };

      return obj;
  });

  container.define("$extend", ["$", "DOMPurify", "logger"], function ($, DOMPurify, logger) {
      var obj = {};

      obj.init = function () {
          if (DOMPurify && DOMPurify instanceof Function) {
              var domPurify = DOMPurify(window);
              $.fn.safeHtml = function (html) {
                  try {
                      this.html(domPurify.sanitize(html));
                  }
                  catch (err) {
                      logger.error(err);
                  }
              };
          }
          else {
              $.fn.safeHtml = function (html) {
                  this.html(html);
              };
          }
      };

      return obj.init(), obj;
  });

  container.define("appRunner", ["router", "logger", "meta", "$"], function (router, logger, meta, $, require) {
      var obj = {};

      obj.run = function (appList) {
          var metaName = "status";
          if (meta.existMeta(metaName)) {
              logger.info("setup already");
          }
          else {
              // 添加meta
              meta.appendMeta(metaName);

              // 运行应用
              $(function () {
                  obj.runAppList(appList);
              });
          }
      };

      obj.runAppList = function (appList) {
          var url = router.getUrl();
          for (var i in appList) {
              var app = appList[i];

              var match = obj.matchApp(url, app);
              if (match == false) {
                  continue;
              }

              if (require(app.name).run() == true) {
                  break;
              }
          }
      };

      obj.matchApp = function (url, app) {
          var match = false;
          app.matchs.forEach(function (item) {
              if (url.indexOf(item) > 0 || item == "*") {
                  match = true;
              }
          });
          return match;
      };

      return obj;
  });

  /** custom **/
  container.define("factory", ["gmDao", "ScopeDao"], function (gmDao, ScopeDao) {
      var obj = {
          daos: {}
      };

      obj.getConfigDao = function () {
          return obj.getDao("config", function () {
              return ScopeDao(gmDao, "$config");
          });
      };

      obj.getStorageDao = function () {
          return obj.getDao("storage", function () {
              return ScopeDao(gmDao, "$storage");
          });
      };

      obj.getDao = function (key, createFunc) {
          if (!obj.daos.hasOwnProperty(key)) {
              obj.daos[key] = createFunc();
          }
          return obj.daos[key];
      };

      return obj;
  });

  container.define("constant", [], function () {
      return {
          source: {
              baidu: "baidu",
              weiyun: "weiyun",
              lanzous: "lanzous",
              ty189: "ty189"
          },
          option: {
              baidu_page_home: {
                  name: "baidu_page_home",
                  value: "yes"
              },
              baidu_page_share: {
                  name: "baidu_page_share",
                  value: "yes"
              },
              baidu_page_verify: {
                  name: "baidu_page_verify",
                  value: "yes"
              },
              baidu_custom_password: {
                  name: "baidu_custom_password",
                  value: "yes"
              },
              baidu_show_origin: {
                  name: "baidu_show_origin",
                  value: "yes"
              },
              baidu_auto_jump: {
                  name: "baidu_auto_jump",
                  value: "no"
              },
              weiyun_page_home: {
                  name: "weiyun_page_home",
                  value: "yes"
              },
              weiyun_page_share: {
                  name: "weiyun_page_share",
                  value: "yes"
              },
              weiyun_page_verify: {
                  name: "weiyun_page_verify",
                  value: "yes"
              },
              weiyun_auto_jump: {
                  name: "weiyun_auto_jump",
                  value: "no"
              },
              lanzous_page_verify: {
                  name: "lanzous_page_verify",
                  value: "yes"
              },
              lanzous_auto_jump: {
                  name: "lanzous_auto_jump",
                  value: "no"
              },
              ty189_page_home: {
                  name: "189_page_home",
                  value: "yes"
              },
              ty189_page_share: {
                  name: "189_page_share",
                  value: "yes"
              },
              ty189_page_verify: {
                  name: "189_page_verify",
                  value: "yes"
              },
              ty189_auto_jump: {
                  name: "189_auto_jump",
                  value: "no"
              }
          }
      };
  });

  container.define("setting", ["config"], function (config) {
      var obj = {};

      obj.getAccessToken = function () {
          var accessToken = config.getConfig("access_token");
          return accessToken ? accessToken : "";
      };

      obj.setAccessToken = function (accessToken) {
          config.setConfig("access_token", accessToken);
      };

      obj.getNotifyStatus = function () {
          var notifyStatus = config.getConfig("notify_status");
          if (!notifyStatus) {
              notifyStatus = "success";
          }
          return notifyStatus;
      };

      obj.setNotifyStatus = function (notifyStatus) {
          config.setConfig("notify_status", notifyStatus);
      };

      obj.showNotifySuccess = function () {
          if (obj.getNotifyStatus() == "all" || obj.getNotifyStatus() == "success") {
              return true;
          }
          else {
              return false;
          }
      };

      obj.showNotifyFail = function () {
          if (obj.getNotifyStatus() == "all" || obj.getNotifyStatus() == "fail") {
              return true;
          }
          else {
              return false;
          }
      };

      return obj;
  });

  container.define("api", ["manifest", "svgCrypt", "oneData"], function (manifest, svgCrypt, oneData) {
      var obj = {};

      obj.versionQuery = function (callback) {
          oneData.requestOneApi(manifest.getApi("version"), {}, callback);
      };

      obj.queryShareOrigin = function (shareSource, shareId, shareLink, callback) {
          var data = {
              share_id: shareId,
              share_source: shareSource,
              share_point: svgCrypt.getStrPoint(shareId),
              share_link: shareLink
          };
          oneData.requestOneApi(manifest.getApi("origin"), data, callback);
      };

      return obj;
  });

  container.define("shareLog", ["config", "calendar", "constant"], function (config, calendar, constant) {
      var obj = {
          name: "share_log_list",
          name_old: "share_list"
      };

      obj.getShareLogList = function (callback) {
          obj.migrateShareLog();

          callback && callback(obj.getLocalShareLogList());
      };

      obj.getLocalShareLogList = function () {
          var shareList = config.getConfig(obj.name);
          return shareList ? shareList : {};
      };

      obj.getShareLog = function (shareSource, shareId, callback) {
          var shareList = obj.getShareLogList();
          var shareNo = obj.buildShareNo(shareSource, shareId);
          if (shareList.hasOwnProperty(shareNo)) {
              callback && callback(shareList[shareNo]);
          }
          else {
              callback && callback(null);
          }
      };

      obj.migrateShareLog = function () {
          try {
              var shareListOld = config.getConfig(obj.name_old);
              if (shareListOld instanceof Object) {
                  var shareList = obj.getLocalShareLogList();
                  for (var i in shareListOld) {
                      var item = shareListOld[i];

                      if (item.share_source == "189") {
                          item.share_source = constant.source.ty189;
                      }

                      shareList[obj.buildShareNo(item.share_source, item.share_id)] = item;
                  }
                  config.setConfig(obj.name, shareList);
                  config.delConfig(obj.name_old);
              }
          }
          catch (err) {
              config.delConfig(obj.name_old);
          }
      };

      obj.addShareLog = function (shareSource, shareId, sharePwd, shareLink, callback) {
          obj.getShareLogList(function (shareList) {
              var shareNo = obj.buildShareNo(shareSource, shareId);
              shareList[shareNo] = {
                  share_id: shareId,
                  share_pwd: sharePwd,
                  share_link: shareLink,
                  share_source: shareSource,
                  share_time: (new Date()).getTime()
              };
              config.setConfig(obj.name, shareList);
              callback && callback();
          });
      };

      obj.removeShareLog = function (shareSource, shareId, callback) {
          obj.getShareLogList(function (shareList) {
              var shareNo = obj.buildShareNo(shareSource, shareId);
              if (shareList.hasOwnProperty(shareNo)) {
                  delete shareList[shareNo];
                  config.setConfig(obj.name, shareList);
              }
              callback && callback();
          });
      };

      obj.buildShareNo = function (shareSource, shareId) {
          return shareSource + "#" + shareId;
      };

      obj.buildShareTime = function (shareTime) {
          return calendar.formatTime("Y-m-d H:i:s", shareTime);
      };

      return obj;
  });

  container.define("runtime", ["router", "manifest", "calendar", "storage", "api"], function (router, manifest, calendar, storage, api) {
      var obj = {};

      obj.openOptionsPage = function () {
          router.openTab(manifest.getOptionsPage(), true);
      };

      obj.initVersion = function () {
          var versionDate = parseInt(storage.getValue("version_date"));
          var currentDate = calendar.formatTime("Ymd");
          if (!versionDate || versionDate < currentDate) {
              api.versionQuery(function (response) {
                  storage.setValue("version_date", currentDate);

                  if (response && response.code == 1 && response.data instanceof Object) {
                      var versionPayload = response.data;
                      storage.setValue("version_payload", versionPayload);
                      storage.setValue("version_latest", versionPayload.version);
                  }
              });
          }
      };

      obj.initRuntime = function () {
          obj.initVersion();
      };

      return obj;
  });

  container.define("core", ["runtime", "$extend"], function (runtime) {
      var obj = {};

      obj.ready = function (callback) {
          runtime.initRuntime();

          callback && callback();
      };

      return obj;
  });

  /** app **/
  container.define("app_baidu", ["manifest", "config", "option", "router", "logger", "unsafeWindow", "constant", "setting", "runtime", "api", "shareLog", "$"], function (manifest, config, option, router, logger, unsafeWindow, constant, setting, runtime, api, shareLog, $) {
      var obj = {
          app_id: 250528,
          temp_path: "/onetmp",
          yun_data: null,
          verify_page: {
              share_pwd: null,
              setPwd: null,
              backupPwd: null,
              restorePwd: null,
              submit_pwd: null
          }
      };

      obj.run = function () {
          var url = router.getUrl();
          if (url.indexOf(".baidu.com/s/") > 0) {
              option.isOptionActive(option.constant.baidu_page_share) && obj.initSharePage();
              return true;
          }
          else if (url.indexOf(".baidu.com/disk/home") > 0) {
              option.isOptionActive(option.constant.baidu_page_home) && obj.initHomePage();
              return true;
          } else if (url.indexOf(".baidu.com/disk/timeline") > 0) {
              option.isOptionActive(option.constant.baidu_page_home) && obj.initTimeLinePage();
              return true;
          } else if (url.indexOf(".baidu.com/share/init") > 0) {
              option.isOptionActive(option.constant.baidu_page_verify) && obj.initVerifyPage();
              return true;
          }
          else {
              return false;
          }
      };

      obj.initSharePage = function () {
          obj.getJquery()(document).ajaxSend(function (event, xhr, options) {
              var clientType = config.getConfig("client_type");
              if (clientType) {
                  options.url = options.url.replace("&clienttype=0", "&clienttype=" + clientType);
              }
          });

          obj.removeVideoLimit();

          obj.prettySingleSharePage();

          obj.initButtonShare();

          obj.initButtonEvent();

          if (option.isOptionActive(option.constant.baidu_show_origin)) {
              obj.showShareOrigin();
          }
      };

      obj.initHomePage = function () {
          obj.registerCustomSharePwd();

          obj.initButtonHome();

          obj.initButtonEvent();
      };

      obj.initTimeLinePage = function () {
          obj.registerCustomSharePwd();

          obj.initButtonTimeLine();

          obj.initButtonEvent();
      };

      obj.initVerifyPage = function () {
          obj.registerStoreSharePwd();

          if (obj.initVerifyPageElement()) {
              obj.autoPaddingSharePwd();
          }
      };

      obj.initVerifyPageElement = function () {
          var shareId = obj.getShareId();
          var $pwd = $(".input-area input");
          if (shareId && $pwd.length) {
              // 设置提取码
              obj.verify_page.setPwd = function (pwd) {
                  $pwd.val(pwd);
              };

              // 备份提取码
              obj.verify_page.backupPwd = function (pwd) {
                  $pwd.attr("data-pwd", pwd);
              };

              // 还原提取码
              obj.verify_page.restorePwd = function () {
                  $pwd.val($pwd.attr("data-pwd"));
              };

              // 提交提取码
              var $button = $(".input-area .g-button-right");
              if ($button.length) {
                  obj.verify_page.submit_pwd = function () {
                      $button.click();
                  };
              }

              return true;
          }
          else {
              return false;
          }
      };

      obj.autoPaddingSharePwd = function () {
          var shareId = obj.getShareId();
          shareLog.getShareLog(constant.source.baidu, shareId, function (record) {
              if (record instanceof Object && record.share_pwd) {
                  var sharePwd = record.share_pwd;
                  obj.verify_page.share_pwd = sharePwd;
                  obj.verify_page.setPwd(sharePwd);
                  setting.showNotifySuccess() && obj.showTipSuccess("[" + manifest.getTitle() + "] 回填提取码成功");

                  if (option.isOptionActive(option.constant.baidu_auto_jump)) {
                      obj.verify_page.submit_pwd && obj.verify_page.submit_pwd();
                  }
              }
              else {
                  setting.showNotifyFail() && obj.showTipError("[" + manifest.getTitle() + "] 没有提取码记录");
              }
          });
      };

      obj.registerStoreSharePwd = function () {
          obj.getJquery()(document).ajaxComplete(function (event, xhr, options) {
              var requestUrl = options.url;
              if (requestUrl.indexOf("/share/verify") >= 0) {
                  var match = options.data.match(/pwd=([a-z0-9]+)/i);
                  if (!match) {
                      return logger.warn("pwd share not match");
                  }

                  // 拒绝*号
                  if (obj.verify_page.backupPwd) {
                      obj.verify_page.backupPwd(match[1]);
                      setTimeout(obj.verify_page.restorePwd, 500);
                  }

                  var response = xhr.responseJSON;
                  if (!(response && response.errno == 0)) {
                      return logger.warn("pwd share error");
                  }

                  var sharePwd = match[1];
                  if (sharePwd == obj.verify_page.share_pwd) {
                      return logger.warn("pwd share not change");
                  }

                  var shareId = obj.getShareId();
                  var shareLink = obj.getShareLink();
                  shareLog.addShareLog(constant.source.baidu, shareId, sharePwd, shareLink);
              }
          });
      };

      obj.registerCustomSharePwd = function () {
          // 功能开关
          if (!option.isOptionActive(option.constant.baidu_custom_password)) {
              return;
          }

          obj.loadPlugin("网盘分享", "com.baidu.pan");

          obj.onModuleReady("function-widget-1:share/util/shareDialog.js", function () {
              // 分享事件
              obj.async("function-widget-1:share/util/shareDialog.js", function (shareDialog) {
                  shareDialog.prototype.onVisibilityChangeOrigin = shareDialog.prototype.onVisibilityChange;
                  shareDialog.prototype.onVisibilityChange = function (status) {
                      if ($(".nd-input-share-pwd").length == 0) {
                          var sharePwd = config.getConfig("share_pwd");
                          var html = '<tr><td class="first-child"><label>提取码</label></td><td><input type="text" class="nd-input-share-pwd" value="' + (sharePwd ? sharePwd : "") + '" placeholder="为空则随机四位" style="padding: 6px; width: 100px;border: 1px solid #e9e9e9;"></td></tr>';
                          $("#share .dialog-body table").append(html);
                      }
                      this.onVisibilityChangeOrigin(status);
                  };
              });

              // 生成提取码
              obj.async("function-widget-1:share/util/shareFriend/createLinkShare.js", function (shareLink) {
                  shareLink.prototype.makePrivatePasswordOrigin = shareLink.prototype.makePrivatePassword;
                  shareLink.prototype.makePrivatePassword = function () {
                      var sharePwd = config.getConfig("share_pwd");
                      return sharePwd ? sharePwd : this.makePrivatePasswordOrigin();
                  };
              });

              // 提取码更改事件
              $(document).on("change", ".nd-input-share-pwd", function () {
                  var value = this.value;
                  if (value && !value.match(/^[0-9a-z]{4}$/i)) {
                      obj.showTipError("提取码只能是四位数字或字母");
                  }
                  config.setConfig("share_pwd", value);
              });
          });
      };

      obj.loadPlugin = function (name, group) {
          try {
              var plugin = obj.require("system-core:pluginHub/data/Registry.js").getPluginByNameAndGroup(name, group);
              obj.require("system-core:pluginHub/invoker/loadPluginAssets.js")(plugin);
          } catch (err) { }
      };

      obj.onModuleReady = function (name, callback) {
          try {
              obj.require(name);
              callback && callback();
          }
          catch (err) {
              setTimeout(function () {
                  obj.onModuleReady(name, callback);
              }, 500);
          }
      };

      obj.removeVideoLimit = function () {
          var message = obj.getSystemContext().message;
          if (message) {
              message.callSystem("share-video-after-transfer");
          }
          else {
              logger.warn("wait removeVideoLimit...");
              obj.setTimeout(obj.removeVideoLimit, 500);
          }
      };

      obj.prettySingleSharePage = function () {
          if (!obj.isSharePageMulti()) {
              $("#layoutMain").css({
                  "width": "auto",
                  "min-width": "1180px",
                  "margin": "88px 30px"
              });
          }
      };

      obj.showShareOrigin = function () {
          api.queryShareOrigin(constant.source.baidu, obj.getShareId(), obj.getShareLink(), function (response) {
              if (response && response.code == 1) {
                  var data = response.data;
                  if (data.list && data.list.length) {
                      var html = '<div style="padding: 10px 5px; border-bottom: 1px solid #f6f6f6; line-height: 30px;">';
                      var item = data.list[0];
                      if (data.list.length > 1) {
                          html += '<p>分享来源：<a target="_blank" href="' + item.url + '">' + item.title + '</a> [<a class="show-origin-dialog" href="javascript:;" style="color:#ff0000;"> 查看更多 </a>]</p>';
                      }
                      else {
                          html += '<p>分享来源：<a target="_blank" href="' + item.url + '">' + item.title + '</a></p>';
                      }
                      html += '</div>';
                      $(".module-share-header").after(html);

                      $(document).on("click", ".show-origin-dialog", function () {
                          var title = "分享来源";
                          var body = '<div style="padding: 20px 20px;min-height: 120px; max-height: 300px; overflow-y: auto;">';

                          data.list.forEach(function (item, index) {
                              body += '<p>' + (++index) + '：<a target="_blank" href="' + item.url + '">' + item.title + '</a></p>';
                          });

                          body += '</div>';
                          var footer = obj.renderFooterAppId();
                          obj.showDialog(title, body, footer);
                      });
                  }
                  else {
                      // obj.showTipError("暂未查询到分享的来源");
                  }
              }
          });
      };

      obj.initButtonShare = function () {
          if ($(".x-button-box").length) {
              var html = '<a class="g-button nd-button-build"><span class="g-button-right"><em class="icon icon-disk" title="下载"></em><span class="text">生成链接</span></span></a>';
              $(".x-button-box").append(html);
          }
          else {
              logger.warn("wait initButtonShare...");
              setTimeout(obj.initButtonShare, 500);
          }
      };

      obj.initButtonHome = function () {
          var listTools = obj.getSystemContext().Broker.getButtonBroker("listTools");
          if (listTools && listTools.$box) {
              var html = '<a class="g-button nd-button-build"><span class="g-button-right"><em class="icon icon-disk" title="下载"></em><span class="text">生成链接</span></span></a>';
              $(listTools.$box).prepend(html);
          }
          else {
              logger.warn("wait initButtonHome...");
              setTimeout(obj.initButtonHome, 500);
          }
      };

      obj.initButtonTimeLine = function () {
          if ($(".module-operateBtn .group-button").length) {
              var html = '<span class="button"><a class="g-v-button g-v-button-middle nd-button-build"><span class="g-v-button-right"><em class="icon icon-disk"></em><span class="text">生成链接</span></span></a></span>';
              $(".module-operateBtn .group-button").prepend(html);
          }
          else {
              logger.warn("wait initButtonTimeLine...");
              setTimeout(obj.initButtonTimeLine, 500);
          }
      };

      obj.initButtonEvent = function () {
          // 生成链接
          $(document).on("click", ".nd-button-build", function () {
              var yunData = obj.getYunData();
              if (yunData.MYUK || obj.isHomePage()) {
                  var fileList = obj.getSelectedFileList();
                  var fileStat = obj.getFileListStat(fileList);
                  if (fileList.length) {
                      if (fileList.length > 1 && fileStat.file_num) {
                          obj.showDownloadSelect(fileList, fileStat);
                      }
                      else if (fileStat.file_num == 1 && !obj.isHomePage()) {
                          obj.showDownloadSingle(fileList, fileStat);
                      }
                      else {
                          var pack = fileStat.file_num ? false : true;
                          if (obj.isHomePage()) {
                              obj.showDownloadInfoHome(fileList, pack);
                          }
                          else {
                              obj.showDownloadInfoShareOffical(fileList, pack);
                          }
                      }
                  }
                  else {
                      obj.showTipError("请至少选择一个文件或文件夹");
                  }
              }
              else {
                  obj.showLogin();
              }
          });

          // 压缩包
          $(document).on("click", ".nd-button-pack", function () {
              var fileList = obj.getSelectedFileList();
              if (obj.isHomePage()) {
                  obj.showDownloadInfoHome(fileList, true);
              }
              else {
                  obj.showDownloadInfoShareOffical(fileList, true);
              }
          });

          // 多文件
          $(document).on("click", ".nd-button-multi", function () {
              var fileList = obj.getSelectedFileList();

              // 过滤文件夹
              fileList = obj.filterFileListDir(fileList);

              if (obj.isHomePage()) {
                  obj.showDownloadInfoHome(fileList, false);
              }
              else {
                  obj.showDownloadInfoShareOffical(fileList, false);
              }
          });

          // 转存多文件
          $(document).on("click", ".nd-button-disk", function () {
              var fileList = obj.getSelectedFileList();

              // 过滤文件夹
              fileList = obj.filterFileListDir(fileList);

              if (obj.isHomePage()) {
                  obj.showDownloadInfoHome(fileList, false);
              }
              else {
                  obj.showDownloadInfoShareTransfer(fileList);
              }
          });

          // 应用ID
          $(document).on("click", ".nd-change-app-id", function () {
              obj.showAppIdChange();
          });
          $(document).on("change", ".nd-input-app-id", function () {
              obj.setAppId(this.value);
          });

          // 打开配置页
          $(document).on("click", ".nd-open-page-option", function () {
              runtime.openOptionsPage();
          });

          // 打开临时页面
          $(document).on("click", ".nd-open-page-temp", function () {
              router.openTab("https://pan.baidu.com/disk/home#/all?vmode=list&path=" + encodeURIComponent(obj.getTempPath()), true);
          });
      };

      obj.showLogin = function () {
          obj.getJquery()("[node-type='header-login-btn']").click();
      };

      obj.showDownloadInfoShareTransfer = function (fileList) {
          logger.info(fileList);
          obj.applyTransferFile(fileList, obj.getTempPath(), function (response) {
              if (response && response.extra && response.extra.list) {
                  var listMap = {};
                  response.extra.list.forEach(function (item) {
                      listMap[item.from_fs_id] = item;
                  });

                  var downList = [];
                  fileList.forEach(function (item) {
                      if (listMap.hasOwnProperty(item.fs_id)) {
                          item.dlink = obj.buildDownloadUrl(listMap[item.fs_id].to, item.server_filename);
                          downList.push(item);
                      }
                  });
                  obj.showDownloadLinkFile(downList);
              }
          });
      };

      obj.showDownloadInfoShareOffical = function (fileList, pack) {
          obj.getDownloadShare(fileList, pack, function (response) {
              obj.hideTip();
              logger.info(response);

              if (response.list && response.list.length) {
                  // 文件
                  obj.showDownloadLinkFile(response.list);
              }
              else if (response.dlink) {
                  // 压缩包
                  obj.showDownloadLinkPack(fileList, {
                      dlink: response.dlink
                  });
              }
              else {
                  // 其他
                  obj.showDialogUnKnownResponse(response);
              }
          });
      };

      obj.showDownloadInfoHome = function (fileList, pack) {
          logger.info(fileList);
          try {
              obj.getDownloadHome(fileList, pack, function (response) {
                  obj.hideTip();
                  logger.info(response);

                  if (pack) {
                      if (response.dlink && typeof response.dlink == "string") {
                          // 压缩包
                          obj.showDownloadLinkPack(fileList, {
                              dlink: response.dlink
                          });
                      }
                      else {
                          // 其他
                          obj.showDialogUnKnownResponse(response);
                      }
                  }
                  else {
                      if (response.dlink instanceof Array && response.dlink.length) {
                          var dlinkMapping = {};
                          response.dlink.forEach(function (item) {
                              dlinkMapping[item.fs_id] = item.dlink;
                          });
                          fileList.forEach(function (item) {
                              item.dlink = dlinkMapping[item.fs_id];
                              item.dlinkApi = obj.buildDownloadUrl(item.path, item.server_filename);
                          });
                      }
                      else {
                          fileList.forEach(function (item) {
                              item.dlink = obj.buildDownloadUrl(item.path, item.server_filename);
                          });
                      }
                      obj.showDownloadLinkFile(fileList);
                  }
              });
          }
          catch (err) {
              fileList.forEach(function (item) {
                  item.dlink = obj.buildDownloadUrl(item.path, item.server_filename);
              });
              obj.showDownloadLinkFile(fileList);
          }
      };

      obj.showDownloadLinkFile = function (fileList) {
          var title = "文件下载";
          var body = '<div style="padding: 20px 20px;min-height: 120px; max-height: 300px; overflow-y: auto; ">';

          var rowStyle = "display:block; overflow:hidden; white-space:nowrap; text-overflow:ellipsis;";
          fileList.forEach(function (item, index) {
              body += '<div style="margin-bottom: 10px;">';
              body += '<div>' + (index + 1) + '：' + item.server_filename + '</div>';
              if (item.dlinkApi) {
                  body += '<div><a href="' + item.dlink + '&filename=' + encodeURIComponent(item.server_filename) + '" title="' + item.dlink + '" style="' + rowStyle + '">官方：' + item.dlink + '</a></div>';
                  body += '<div><a href="' + item.dlinkApi + '&filename=' + encodeURIComponent(item.server_filename) + '" title="' + item.dlinkApi + '" style="' + rowStyle + '">直链：' + item.dlinkApi + '</a></div>';
              }
              else {
                  body += '<div><a href="' + item.dlink + '&filename=' + encodeURIComponent(item.server_filename) + '" title="' + item.dlink + '" style="' + rowStyle + '">' + item.dlink + '</a></div>';
              }
              body += '</div>';
          });

          body += '</div>';
          var footer = obj.renderFooterAppId();
          obj.showDialog(title, body, footer);
      };

      obj.showDownloadLinkPack = function (fileList, data) {
          var title = "文件下载";
          var body = '<div style="padding: 20px 20px;min-height: 120px; max-height: 300px; overflow-y: auto; ">';

          var packName = obj.getDownloadPackName(fileList);
          body += '<div>' + packName + '</div><div><a href="' + data.dlink + '&zipname=' + encodeURIComponent(packName) + '" title="' + data.dlink + '" style="display:block; overflow:hidden; white-space:nowrap; text-overflow:ellipsis;">' + data.dlink + '</a></div>';

          body += '<div style="margin-top: 15px;">打包的文件/文件夹列表</div>';
          fileList.forEach(function (item, index) {
              body += '<div title="' + item.path + '" style="color: ' + (item.isdir ? "blue" : "inherit") + ';">[' + (index + 1) + '] ' + item.server_filename + '</div>';
          });

          body += '</div>';
          var footer = obj.renderFooterAppId();
          obj.showDialog(title, body, footer);
      };

      obj.getDownloadPackName = function (fileList) {
          return fileList[0].server_filename + " 等" + fileList.length + "个文件.zip";
      };

      obj.buildDownloadUrl = function (path, name) {
          return "https://pcs.baidu.com/rest/2.0/pcs/file?method=download&app_id=" + obj.getAppId() + "&filename=" + encodeURIComponent(name) + "&path=" + encodeURIComponent(path);
      };

      obj.showDownloadSingle = function (fileList, fileStat) {
          var title = "链接类型";
          var body = '<div style="padding: 40px 20px; max-height: 300px; overflow-y: auto;">';

          body += '<div class="normalBtnBox g-center">';
          body += '<a class="g-button g-button-large g-button-gray-large nd-button-multi" title="调用官方接口生成链接"><span class="g-button-right"><em class="icon icon-download"></em> 官方链接</span></a>';
          body += '<a class="g-button g-button-large g-button-gray-large nd-button-disk" style="margin-left:50px;" title="转存文件然后生成文件直链"><span class="g-button-right"><em class="icon icon-save-disk"></em> 转存直链</span></a>';
          body += '</div>';

          if (fileStat.dir_num) {
              body += '<div style="margin-top: 40px; padding-top: 10px; margin-bottom: -20px; border-top: 1px solid #D0DFE7;"><p class="g-center">选择 [多文件] 会过滤当前选中的 <span style="color: red">' + fileStat.dir_num + '</span> 个文件夹</p>';

              var index = 1;
              fileList.forEach(function (item) {
                  if (item.isdir) {
                      body += '<p title="' + item.path + '" style="color: blue;">[' + index + '] ' + item.server_filename + '</p>';
                      index++;
                  }
              });
              body += '</div>';
          }

          body += '</div>';
          var footer = obj.renderFooterAppId();
          obj.showDialog(title, body, footer);
      };

      obj.showDownloadSelect = function (fileList, fileStat) {
          var title = "链接类型";
          var body = '<div style="padding: 40px 20px; max-height: 300px; overflow-y: auto;">';

          body += '<div class="normalBtnBox g-center">';
          if (obj.isHomePage()) {
              body += '<a class="g-button g-button-large g-button-gray-large nd-button-disk" title="合并官方链接和文件直链"><span class="g-button-right"><em class="icon icon-save-disk"></em> 多文件</span></a>';
          }
          else {
              body += '<a class="g-button g-button-large g-button-gray-large nd-button-multi"><span class="g-button-right" title="调用官方接口生成文件链接"><em class="icon icon-download"></em> 官方多文件</span></a>';
              body += '<a class="g-button g-button-large g-button-gray-large nd-button-disk" style="margin-left:50px;" title="转存文件然后生成文件直链"><span class="g-button-right"><em class="icon icon-save-disk"></em> 转存多文件</span></a>';
          }
          body += '<a class="g-button g-button-large g-button-gray-large nd-button-pack" style="margin-left:50px;" title="调用官方接口生成压缩包链接"><span class="g-button-right"><em class="icon icon-poly"></em> 压缩包</span></a>';
          body += '</div>';

          if (fileStat.dir_num) {
              body += '<div style="margin-top: 40px; padding-top: 10px; margin-bottom: -20px; border-top: 1px solid #D0DFE7;"><p class="g-center">选择 [多文件] 会过滤当前选中的 <span style="color: red">' + fileStat.dir_num + '</span> 个文件夹</p>';
              var index = 1;
              fileList.forEach(function (item) {
                  if (item.isdir) {
                      body += '<p title="' + item.path + '" style="color: blue;">[' + index + '] ' + item.server_filename + '</p>';
                      index++;
                  }
              });
              body += '</div>';
          }

          body += '</div>';
          var footer = obj.renderFooterAppId();
          obj.showDialog(title, body, footer);
      };

      obj.showAppIdChange = function () {
          var title = "应用ID";
          var body = '<div style="padding: 60px 20px; max-height: 300px; overflow-y: auto;"><div class="g-center" style="margin-bottom: 10px;">当前应用ID：<input type="text" class="nd-input-app-id" style="border: 1px solid #f2f2f2; padding: 4px 5px;" value="' + obj.getAppId() + '"></div><div class="g-center"><p>用于构造个人网盘文件的下载直链，更多应用ID请查看<a target="_blank" href="http://go.newday.me/s/pan-script"> 脚本主页 </a></p></div></div>';
          var footer = '';
          obj.showDialog(title, body, footer);
      };

      obj.showDialogUnKnownResponse = function (response) {
          var title = "未知结果";
          var body = '<div style="padding: 20px 20px; max-height: 300px; overflow-y: auto;"><pre style="white-space: pre-wrap; word-wrap: break-word; word-break: break-all;">' + JSON.stringify(response, null, 4) + '</pre></div>';
          var footer = obj.renderFooterAppId();
          obj.showDialog(title, body, footer);
      };

      obj.renderFooterAppId = function () {
          return '<p style="padding-top: 10px; border-top: 1px solid #D0DFE7;">应用ID：' + obj.getAppId() + ' <a href="javascript:;" class="nd-change-app-id">修改</a>，其他页面： <a class="nd-open-page-option" href="javascript:;">配置页面</a> 、<a class="nd-open-page-temp" href="javascript:;">临时文件</a></p>';
      };

      obj.showDialog = function (title, body, footer) {
          var dialog = obj.require("system-core:system/uiService/dialog/dialog.js").verify({
              title: title,
              img: "img",
              vcode: "vcode"
          });

          // 内容
          $(dialog.$dialog).find(".dialog-body").safeHtml(body);

          // 底部
          $(dialog.$dialog).find(".dialog-footer").safeHtml(footer);

          dialog.show();
      };

      obj.showTipSuccess = function (msg, hasClose, autoClose) {
          obj.showTip("success", msg, hasClose, autoClose);
      };

      obj.showTipError = function (msg, hasClose, autoClose) {
          obj.showTip("failure", msg, hasClose, autoClose);
      };

      obj.showTipLoading = function (msg, hasClose, autoClose) {
          obj.showTip("loading", msg, hasClose, autoClose);
      };

      obj.showTip = function (mode, msg, hasClose, autoClose) {
          var option = {
              mode: mode,
              msg: msg
          };

          // 关闭按钮
          if (typeof hasClose != "undefined") {
              option.hasClose = hasClose;
          }

          // 自动关闭
          if (typeof autoClose != "undefined") {
              option.autoClose = autoClose;
          }

          obj.require("system-core:system/uiService/tip/tip.js").show(option);
      };

      obj.hideTip = function () {
          obj.require("system-core:system/uiService/tip/tip.js").hide({
              hideTipsAnimationFlag: 1
          });
      };

      obj.isHomePage = function () {
          var url = router.getUrl();
          if (url.indexOf(".baidu.com/disk") > 0) {
              return true;
          }
          else {
              return false;
          }
      };

      obj.isTimelinePage = function () {
          var url = router.getUrl();
          if (url.indexOf(".baidu.com/disk/timeline") > 0) {
              return true;
          }
          else {
              return false;
          }
      };

      obj.isSharePageMulti = function () {
          var yunData = obj.getYunData();
          if (yunData.SHAREPAGETYPE == "single_file_page") {
              return false;
          }
          else {
              return true;
          }
      };

      obj.getSelectedFileList = function () {
          if (obj.isHomePage()) {
              return obj.getSelectedFileListHome();
          }
          else {
              return obj.getSelectedFileListShare();
          }
      };

      obj.getSelectedFileListHome = function () {
          if (obj.isTimelinePage()) {
              return obj.require("pan-timeline:widget/store/index.js").getters.getChoosedItemArr;
          }
          else {
              return obj.require('system-core:context/context.js').instanceForSystem.list.getSelected();
          }
      };

      obj.getSelectedFileListShare = function () {
          return obj.require('system-core:context/context.js').instanceForSystem.list.getSelected();
      };

      obj.getFileListStat = function (fileList) {
          var fileStat = {
              file_num: 0,
              dir_num: 0
          };
          fileList.forEach(function (item) {
              if (item.isdir == 0) {
                  fileStat.file_num++;
              }
              else {
                  fileStat.dir_num++;
              }
          });
          return fileStat;
      };

      obj.filterFileListDir = function (fileList) {
          var fileListFilter = [];
          fileList.forEach(function (item) {
              if (item.isdir == 0) {
                  fileListFilter.push(item);
              }
          });
          return fileListFilter;
      };

      obj.parseFidList = function (fileList) {
          var fidList = [];
          fileList.forEach(function (item) {
              fidList.push(item.fs_id);
          });
          return fidList;
      };

      obj.getDownloadShare = function (fileList, pack, callback) {
          obj.showTipLoading("生成链接中，请稍等...");

          obj.loadPlugin("网盘下载", "com.baidu.pan");

          obj.onModuleReady("function-widget-1:download/util/context.js", function () {

              obj.initWidgetContext("function-widget-1:download/util/context.js");

              obj.async("function-widget-1:download/service/dlinkService.js", function (dl) {
                  var yunData = obj.getYunData();
                  var data = {
                      list: fileList,
                      share_uk: yunData.SHARE_UK,
                      share_id: yunData.SHARE_ID,
                      sign: yunData.SIGN,
                      timestamp: yunData.TIMESTAMP,
                      type: pack ? "batch" : "nolimit"
                  };
                  dl.getDlinkShare(data, callback);
              });
          });
      };

      obj.getDownloadHome = function (fileList, pack, callback) {
          obj.showTipLoading("生成链接中，请稍等...");

          obj.loadPlugin("网盘下载", "com.baidu.pan");

          obj.onModuleReady("function-widget-1:download/util/context.js", function () {

              obj.initWidgetContext("function-widget-1:download/util/context.js");

              obj.async("function-widget-1:download/service/dlinkService.js", function (dl) {
                  var fidList = obj.parseFidList(fileList);
                  var type = pack ? "batch" : "nolimit";
                  dl.getDlinkPan(JSON.stringify(fidList), type, callback);
              });
          });
      };

      obj.applyTransferFile = function (fileList, path, callback) {
          obj.listDir(path, function (response) {
              if (response && response.errno == 0) {
                  obj.transferFile(fileList, path, callback);
              }
              else if (response) {
                  obj.createDir(path, function (response) {
                      if (response && response.errno == 0) {
                          obj.transferFile(fileList, response.path, callback);
                      }
                      else {
                          callback && callback("");
                      }
                  });
              }
              else {
                  callback && callback("");
              }
          });
      };

      obj.transferFile = function (fileList, path, callback) {
          var yunData = obj.getYunData();
          var fidList = obj.parseFidList(fileList);
          var url = "/share/transfer?ondup=newcopy&async=1&shareid=" + yunData.SHARE_ID + "&from=" + yunData.SHARE_UK;
          var data = {
              fsidlist: "[" + fidList.join(",") + "]",
              path: path
          };
          obj.ajax({
              type: "post",
              url: url,
              data: data,
              dataType: "json",
              timeout: 1e5,
              error: function () {
                  callback && callback("");
              },
              success: function (response) {
                  callback && callback(response);
              }
          });
      };

      obj.listDir = function (path, callback) {
          var url = "/api/list";
          obj.ajax({
              type: "get",
              url: url,
              data: {
                  order: "name",
                  desc: 0,
                  showempty: 0,
                  web: 1,
                  page: 1,
                  num: 10,
                  dir: path
              },
              dataType: "json",
              timeout: 1e5,
              error: function () {
                  callback && callback("");
              },
              success: function (response) {
                  callback && callback(response);
              }
          });
      };

      obj.createDir = function (path, callback) {
          var url = "/api/create?a=commit";
          obj.ajax({
              type: "post",
              url: url,
              data: {
                  path: path,
                  isdir: 1,
                  block_list: "[]"
              },
              dataType: "json",
              timeout: 1e5,
              error: function () {
                  callback && callback("");
              },
              success: function (response) {
                  callback && callback(response);
              }
          });
      };

      obj.getShareId = function () {
          var match;

          match = location.href.match(/share\/init\?surl=([a-z0-9-_]+)/i);
          if (match) {
              return match[1];
          }

          match = location.pathname.match(/\/s\/1([a-z0-9-_]+)/i);
          if (match) {
              return match[1];
          }

          return null;
      };

      obj.getShareLink = function () {
          return router.getUrl();
      };

      obj.getYunData = function () {
          if (!obj.yun_data) {
              obj.yun_data = unsafeWindow.yunData;
          }
          return obj.yun_data;
      };

      obj.getTempPath = function () {
          var tempPath = config.getConfig("temp_path");
          if (tempPath) {
              return tempPath;
          }
          else {
              return obj.temp_path;
          }
      };

      obj.setTempPath = function (tempPath) {
          config.setConfig("temp_path", tempPath);
      };

      obj.getAppId = function () {
          var appId = config.getConfig("app_id");
          if (appId) {
              return appId;
          }
          else {
              return obj.app_id;
          }
      };

      obj.setAppId = function (appId) {
          config.setConfig("app_id", appId);
      };

      obj.initWidgetContext = function (name) {
          try {
              obj.async(name, function (widget) {
                  widget.setContext(obj.getSystemContext());
              });
          }
          catch (err) { }
      };

      obj.ajax = function (option) {
          obj.getJquery().ajax(option);
      };

      obj.getSystemContext = function () {
          return obj.require("system-core:context/context.js").instanceForSystem;
      };

      obj.getJquery = function () {
          return obj.require("base:widget/libs/jquerypacket.js");
      };

      obj.require = function (name) {
          return unsafeWindow.require(name);
      };

      obj.async = function (name, callback) {
          unsafeWindow.require.async(name, callback);
      };

      return obj;
  });

  container.define("app_weiyun", ["manifest", "router", "option", "logger", "unsafeWindow", "constant", "setting", "shareLog", "$"], function (manifest, router, option, logger, unsafeWindow, constant, setting, shareLog, $) {
      var obj = {
          modules: {},
          webpack_require: null,
          verify_page: {
              setPwd: null,
              share_pwd: null,
              submit_pwd: null
          }
      };

      obj.run = function () {
          var url = router.getUrl();
          if (url.indexOf("weiyun.com/disk") > 0) {
              option.isOptionActive(option.constant.weiyun_page_home) && obj.initHomePage();
              return true;
          }
          else if (url.indexOf("share.weiyun.com") > 0) {
              obj.initVerifyPage();
              return true;
          }
          else {
              return false;
          }
      };

      obj.initHomePage = function () {
          obj.initWebpackRequire();

          setInterval(obj.initHomePageElement, 1000);
      };

      obj.initHomePageElement = function () {
          var template = '<div class="action-item mod-action-wrap-link"><div class="action-item-con"><i class="icon icon-link"></i><span class="act-txt">显示链接</span></div></div>';
          $(".mod-action-wrap-menu:not(.nd-show-link-already)").each(function () {
              var $this = $(this);
              if ($this.find(".icon-download")) {
                  $this.addClass("nd-show-link-already");

                  $this.prepend(template);
                  $this.find(".mod-action-wrap-link").click(function (e) {
                      e.stopPropagation();
                      obj.showHomeDownload();
                  });
              }
          });
      };

      obj.initVerifyPage = function () {
          obj.initWebpackRequire();

          if (option.isOptionActive(option.constant.weiyun_page_verify)) {
              obj.registerStoreSharePwd();

              obj.initVerifyPageElement(function () {
                  obj.autoPaddingSharePwd();
              });
          }

          if (option.isOptionActive(option.constant.weiyun_page_share) && unsafeWindow.syncData.shareInfo.note_list.length == 0) {
              obj.initSharePage();
          }
      };

      obj.initSharePage = function () {
          if ($(".mod-action-wrap-link").length == 0) {
              var html = '<div class="mod-action-wrap mod-action-wrap-menu mod-action-wrap-link clearfix"><div class="action-item"><div class="action-item-con"><i class="icon icon-link"></i><span class="act-txt">显示链接</span></div></div></div>';
              $(".mod-action-wrap-code").after(html);

              $(".mod-action-wrap-link").click(function (e) {
                  e.stopPropagation();
                  obj.showShareDownload();
              });
          }
          setTimeout(obj.initSharePage, 500);
      };

      obj.initVerifyPageElement = function (callback) {
          var shareId = obj.getShareId();
          var $pwd = $(".card-inner .input-txt");
          var $button = $(".card-inner .btn-main");
          if (shareId && $pwd.length && $button.length) {

              // 显示分享密码
              $pwd.attr("type", "text");

              // 设置分享密码
              obj.verify_page.setPwd = function (pwd) {
                  $pwd.val(pwd);
              };

              // 重造按钮
              var $itemButton = $button.parent();
              $itemButton.safeHtml($button.prop("outerHTML"));
              $button = $itemButton.find(".btn-main");

              // 按钮事件
              $button.on("click", function () {
                  obj.getStore() && obj.getStore().dispatch("shareInfo/loadShareInfoWithoutLogin", $pwd.val());
              });

              // 提交密码
              obj.verify_page.submit_pwd = function () {
                  $button.click();
              };

              callback && callback();
          }
          else {
              setTimeout(function () {
                  obj.initVerifyPageElement(callback);
              }, 500);
          }
      };

      obj.autoPaddingSharePwd = function () {
          var shareId = obj.getShareId();
          shareLog.getShareLog(constant.source.weiyun, shareId, function (record) {
              if (record instanceof Object && record.share_pwd) {
                  var sharePwd = record.share_pwd;
                  obj.verify_page.share_pwd = sharePwd;
                  obj.verify_page.setPwd(sharePwd);
                  setting.showNotifySuccess() && obj.showTipSuccess("[" + manifest.getTitle() + "] 回填密码成功");

                  if (option.isOptionActive(option.constant.weiyun_auto_jump)) {
                      obj.verify_page.submit_pwd && obj.verify_page.submit_pwd();
                  }
              }
              else {
                  setting.showNotifyFail() && obj.showTipError("[" + manifest.getTitle() + "] 没有密码记录");
              }
          });
      };

      obj.registerStoreSharePwd = function () {
          obj.addResponseInterceptor(function (request, response) {
              var requestUrl = request.responseURL;
              if (requestUrl.indexOf("weiyunShareNoLogin/WeiyunShareView") > 0) {
                  if (response.data.data.rsp_header.retcode == 0) {
                      var match = response.config.data.match(/\\"share_pwd\\":\\"([\w]+)\\"/);
                      if (!match) {
                          return logger.warn("pwd share not match");
                      }

                      var sharePwd = match[1];
                      if (sharePwd == obj.verify_page.share_pwd) {
                          return logger.warn("pwd share not change");
                      }

                      var shareId = obj.getShareId();
                      var shareLink = obj.getShareLink();
                      shareLog.addShareLog(constant.source.weiyun, shareId, sharePwd, shareLink);
                  }
                  else {
                      return logger.warn("pwd share error");
                  }
              }
          });
      };

      obj.addResponseInterceptor = function (callback) {
          var success = function (response) {
              try {
                  callback && callback(response.request, response);
              }
              catch (e) {
                  logger.warn(e);
              }
              return response;
          };
          var error = function () {
              return Promise.reject(error);
          };
          obj.getAxios() && obj.getAxios().interceptors.response.use(success, error);
      };

      obj.showBox = function (body) {
          var template = '<div class="modal modal-show" id="file-modal"><b class="modal-mask"></b><div class="modal-dialog modal-dialog-680"><div class="modal-dialog-hd clearfix"><h4 class="modal-dialog-title">文件下载</h4><button class="btn-icon icon icon-pop-close"></button></div><div class="modal-dialog-bd modal-body"></div></div></div>';
          if ($("#file-modal").length == 0) {
              $("body").append(template);
              $("#file-modal .icon-pop-close").on("click", function () {
                  $("#file-modal").hide();
              });
          }
          $("#file-modal").show();
          $("#file-modal .modal-body").safeHtml(body);
      };

      obj.showShareDownload = function () {
          var fileData = obj.getSelectedShareFileData();
          if (fileData.node_list.length == 0) {
              return obj.showTipError("请选择至少一个文件/文件夹");
          }

          obj.requestShareDownload(fileData).then(function (response) {
              obj.showShareDownloadBox(fileData, response);
          }, function (response) {
              obj.showTipError(response.msg);
          });
      };

      obj.showHomeDownload = function () {
          var fileData = obj.getSelectedShareFileData();
          if (fileData.node_list.length == 0) {
              return obj.showTipError("请选择至少一个文件/文件夹");
          }

          obj.requestHomeDownload(fileData).then(function (response) {
              obj.showShareDownloadBox(fileData, response);
          }, function (response) {
              obj.showTipError(response.msg);
          });
      };

      obj.parseDownFile = function (fileData) {
          var fileName = "", packName = "";
          if (fileData.dir_list.length > 0) {
              if (fileData.file_list.length > 0) {
                  packName = fileData.dir_list[0].filename + " 等" + (fileData.dir_list.length + fileData.file_list.length) + "个文件";
              }
              else {
                  packName = fileData.dir_list[0].filename;
              }
              fileName = packName + ".zip";
          }
          else {
              if (fileData.file_list.length > 1) {
                  packName = fileData.node_list[0].getNameNoExt() + " 等" + fileData.file_list.length + "个文件";
                  fileName = packName + ".zip";
              }
              else {
                  fileName = fileData.file_list[0].filename;
              }
          }
          return {
              file_name: fileName,
              pack_name: packName
          };
      };

      obj.requestHomeDownload = function (fileData) {
          var baseRequest = obj.getBaseRequest();
          var downFile = obj.parseDownFile(fileData);
          if (baseRequest) {
              return downFile.pack_name ? baseRequest.getPackUrl(fileData.node_list, {}) : baseRequest.getSingleUrl(fileData.node_list, {});
          }
          else {
              return new Promise(function (resolve, reject) {
                  reject({ retcode: -1, msg: "生成链接失败" });
              });
          }
      };

      obj.requestShareDownload = function (fileData) {
          var shareFile = obj.getShareFile(), downloadRequest = obj.getDownloadRequest();
          var downFile = obj.parseDownFile(fileData);
          if (shareFile && downloadRequest) {
              var detail = {
                  shareKey: shareFile.shareKey,
                  sharePwd: shareFile.sharePwd,
                  fileOwner: shareFile.shareOwner,
                  downloadType: 0,
                  packName: downFile.pack_name,
                  pdirKey: "",
                  dirList: fileData.dir_list,
                  fileList: fileData.file_list
              };
              return downFile.pack_name ? downloadRequest.sharePartDownload(detail) : downloadRequest.shareBatchDownload(detail);
          }
          else {
              return new Promise(function (resolve, reject) {
                  reject({ retcode: -1, msg: "生成链接失败" });
              });
          }
      };

      obj.showShareDownloadBox = function (fileData, response) {
          var downFile = obj.parseDownFile(fileData);
          if (response.download_url) {
              Object.assign(downFile, response);
          }
          else {
              Object.assign(downFile, response.file_list[0]);
          }

          var html = '<div style="padding: 20px; overflow-y: auto;">';
          var rowStyle = "margin:10px 0px;overflow:hidden; white-space:nowrap; text-overflow:ellipsis;";
          html += '<p>' + downFile.file_name + '</p>';
          html += '<p style="' + rowStyle + '"><a title="' + downFile.download_url + '" href="' + downFile.download_url + '" style="color: blue;">' + downFile.download_url + '</a></p>';
          html += '<div>';
          obj.showBox(html);
      };

      obj.showTipSuccess = function (msg) {
          obj.getModal() && obj.getModal().success(msg);
      };

      obj.showTipError = function (msg) {
          obj.getModal() && obj.getModal().error(msg);
      };

      obj.getShareId = function () {
          var url = obj.getShareLink();
          var match = url.match(/share.weiyun.com\/([0-9a-z]+)/i);
          return match ? match[1] : null;
      };

      obj.getShareLink = function () {
          return router.getUrl();
      };

      obj.isHomePage = function () {
          if (router.getUrl().indexOf("weiyun.com/disk") >= 0) {
              return true;
          }
          else {
              return false;
          }
      };

      obj.getSelectedShareFileData = function () {
          var fileData = {
              node_list: obj.getSelectedFileNodes(),
              dir_list: [],
              file_list: []
          };
          fileData.node_list.forEach(function (item) {
              if (item.getSize) {
                  var file = {
                      file_id: item.getId(),
                      pdir_key: item.getPdirKey(),
                      filename: item.getName(),
                      file_size: item.getSize()
                  };
                  if (item.isDir()) {
                      fileData.dir_list.push(file);
                  }
                  else {
                      fileData.file_list.push(file);
                  }
              }
          });
          return fileData;
      };

      obj.getSelectedFileNodes = function () {
          var fileNodes = [];
          if (obj.isHomePage()) {
              fileNodes = obj.getHomeFileNodes();
          }
          else {
              var shareFile = obj.getShareFile();
              if (shareFile) {
                  if (shareFile.isSingleFile) {
                      fileNodes = shareFile.childNodes;
                  }
                  else {
                      fileNodes = shareFile.selectedNodes;
                  }
              }
          }
          return fileNodes;
      };

      obj.getHomeFileNodes = function () {
          var fileNodes = [];
          var store = obj.getStore();
          var url = location.href;
          var filter = function (node) {
              return node.isSelected() ? 1 : 0;
          };
          if (store instanceof Object) {
              if (url.indexOf("weiyun.com/disk/doc") >= 0) {
                  fileNodes = store.state.doc.curCateNode.getKidNodes().filter(filter);
              }
              else if (url.indexOf("weiyun.com/disk/photo") >= 0) {
                  fileNodes = store.state.photo.curCateNode.getKidNodes().filter(filter);
              }
              else if (url.indexOf("weiyun.com/disk/video") >= 0) {
                  fileNodes = store.state.video.cateNode.getKidNodes().filter(filter);
              }
              else if (url.indexOf("weiyun.com/disk/auido") >= 0) {
                  fileNodes = store.state.audio.cateNode.getKidNodes().filter(filter);
              }
              else if (url.indexOf("weiyun.com/disk/time") >= 0) {
                  fileNodes = store.state.time.rootNode.getKidNodes().filter(filter);
              }
              else if (url.indexOf("weiyun.com/disk/sharedir") >= 0) {
                  fileNodes = store.state.sharedir.curNode.getKidNodes().filter(filter);
              }
              else if (url.indexOf("weiyun.com/disk/recent") >= 0) {
                  var kidFeeds = store.state.recent.rootNode.getKidFeeds();
                  kidFeeds.forEach(function (feed) {
                      if (feed.isSelected()) {
                          fileNodes = fileNodes.concat(feed.getKidNodes());
                      }
                  });
              }
              else if (url.indexOf("weiyun.com/disk/recycle") >= 0) {
                  fileNodes = store.state.recycle.rootNode.getKidNodes().filter(filter);
              }
              else if (store.state.disk) {
                  fileNodes = store.state.disk.curNode.getKidNodes().filter(filter);
              }
          }
          return fileNodes;
      };

      obj.getShareFile = function () {
          var store = obj.getStore();
          if (store instanceof Object) {
              return store.state.sharefile.shareFile;
          }
      };

      obj.getBaseRequest = function () {
          return obj.matchWebpackModule("base_request", function (module, name) {
              if (module && module.getSingleUrl) {
                  return module;
              }
          });
      };

      obj.getDownloadRequest = function () {
          return obj.matchWebpackModule("download_request", function (module, name) {
              if (module && module.DownloadRequest) {
                  return new module.DownloadRequest();
              }
          });
      };

      obj.getAxios = function () {
          return obj.matchWebpackModule("axios", function (module, name) {
              if (module && module.Axios) {
                  return module;
              }
          });
      };

      obj.getModal = function () {
          return obj.matchWebpackModule("modal", function (module, name) {
              if (module && module.confirm && module.success) {
                  return module;
              }
          });
      };

      obj.getStore = function () {
          return obj.matchWebpackModule("store", function (module, name) {
              if (module && module.default && module.default._modulesNamespaceMap) {
                  return module.default;
              }
          });
      };

      obj.matchWebpackModule = function (name, matchFunc) {
          if (!obj.modules.hasOwnProperty(name)) {
              for (var key in obj.webpack_require.c) {
                  var match = matchFunc(obj.webpack_require(key), key);
                  if (match) {
                      obj.modules[name] = match;
                  }
              }
          }
          return obj.modules[name];
      };

      obj.initWebpackRequire = function () {
          var injectName = "_nd_inject_";
          var moreModules = {};
          moreModules[injectName] = function (module, exports, __webpack_require__) {
              obj.webpack_require = __webpack_require__;
          };
          unsafeWindow.webpackJsonp([injectName], moreModules, [injectName]);
      };

      return obj;
  });

  container.define("app_lanzous", ["manifest", "router", "option", "logger", "unsafeWindow", "constant", "setting", "shareLog", "$"], function (manifest, router, option, logger, unsafeWindow, constant, setting, shareLog, $) {
      var obj = {
          verify_page: {
              setPwd: null,
              share_pwd: null,
              submit_pwd: null
          }
      };

      obj.run = function () {
          var url = router.getUrl();
          if (url.indexOf("lanzous.com") > 0 || url.indexOf("lanzoux.com") > 0) {
              option.isOptionActive(option.constant.lanzous_page_verify) && obj.initVerifyPage();
              return true;
          }
          else {
              return false;
          }
      };

      obj.initVerifyPage = function () {
          obj.registerStoreSharePwd();

          obj.initVerifyPageElement(function () {
              obj.autoPaddingSharePwd();
          });
      };

      obj.initVerifyPageElement = function (callback) {
          var shareId = obj.getShareId();
          var $pwd = $("#pwd");
          if (shareId && $pwd.length) {

              // 设置分享密码
              obj.verify_page.setPwd = function (pwd) {
                  $pwd.val(pwd);
              };

              // 提交密码
              obj.verify_page.submit_pwd = function () {
                  $("#sub").click();
                  unsafeWindow.down_p && unsafeWindow.down_p();
              };

              callback && callback();
          }
          else {
              setTimeout(function () {
                  obj.initVerifyPageElement(callback);
              }, 500);
          }
      };

      obj.autoPaddingSharePwd = function () {
          var shareId = obj.getShareId();
          shareLog.getShareLog(constant.source.lanzous, shareId, function (record) {
              if (record instanceof Object && record.share_pwd) {
                  var sharePwd = record.share_pwd;
                  obj.verify_page.share_pwd = sharePwd;
                  obj.verify_page.setPwd(sharePwd);
                  setting.showNotifySuccess() && obj.showTip(1, "[" + manifest.getTitle() + "] 回填密码成功", 2000);

                  if (option.isOptionActive(option.constant.lanzous_auto_jump)) {
                      obj.verify_page.submit_pwd && obj.verify_page.submit_pwd();
                  }
              }
              else {
                  setting.showNotifyFail() && obj.showTip(0, "[" + manifest.getTitle() + "] 没有密码记录", 2000);
              }
          });
      };

      obj.registerStoreSharePwd = function () {
          unsafeWindow.$(document).ajaxComplete(function (event, xhr, options) {
              var match = options.data.match(/pwd=(\w+)/);
              if (!match) {
                  match = options.data.match(/p=(\w+)/);
                  if (!match) {
                      return logger.warn("pwd share not match");
                  }
              }

              var sharePwd = match[1];
              if (sharePwd == obj.verify_page.share_pwd) {
                  return logger.warn("pwd share not change");
              }

              var shareId = obj.getShareId();
              var shareLink = obj.getShareLink();
              var response = obj.parseJson(xhr.response);
              if (response && response.zt == 1 && sharePwd) {
                  shareLog.addShareLog(constant.source.lanzous, shareId, sharePwd, shareLink);
              }
              else {
                  return logger.warn("pwd share error");
              }
          });
      };

      obj.showTip = function (code, msg, timeout) {
          if (unsafeWindow.sms) {
              unsafeWindow.sms(msg);
          }
          else {
              var selector;
              if ($(".off").length) {
                  selector = "#pwderr";
              }
              else {
                  selector = "#info";
              }
              if (code) {
                  $(selector).safeHtml('<span style="color: green;">' + msg + '</span>');
              }
              else {
                  $(selector).safeHtml('<span style="color: red;">' + msg + '</span>');
              }
              setTimeout(function () {
                  $(selector).text("");
              }, timeout);
          }
      };

      obj.getShareId = function () {
          var url = obj.getShareLink();
          var match;

          match = /[lanzous|lanzoux].com\/([\w]+)\/([a-z0-9-_]{4,})/gi.exec(url);
          if (match) {
              return match[1] + "/" + match[2];
          }

          match = /[lanzous|lanzoux].com\/([a-z0-9-_]{4,})/gi.exec(url);
          if (match) {
              return match[1];
          }

          return null;
      };

      obj.getShareLink = function () {
          return router.getUrl();
      };

      obj.parseJson = function (jsonStr) {
          var jsonObject = {};
          try {
              if (jsonStr) {
                  jsonObject = JSON.parse(jsonStr);
              }
          }
          catch (e) { }
          return jsonObject;
      };

      return obj;
  });

  container.define("app_189", ["manifest", "router", "option", "logger", "unsafeWindow", "constant", "setting", "shareLog", "$"], function (manifest, router, option, logger, unsafeWindow, constant, setting, shareLog, $) {
      var obj = {
          verify_page: {
              share_pwd: null
          }
      };

      obj.run = function () {
          var url = router.getUrl();
          if (url.indexOf("cloud.189.cn/t") > 0) {
              obj.initSharePage();
              return true;
          }
          else if (url.indexOf("cloud.189.cn/main") > 0 || url.indexOf("cloud.189.cn/photo") > 0) {
              option.isOptionActive(option.constant.ty189_page_home) && obj.initHomePage();
              return true;
          }
          else {
              return false;
          }
      };

      obj.initHomePage = function () {
          if ($("#J_Create").length) {
              $("#J_Create").after('<a class="btn btn-show-link" style="background: #2b89ea; color: #fff; cursor: pointer">显示链接</a>');
              $(".btn-show-link").on("click", obj.showDownload);
          }
          else if ($(".JC_Refresh").length) {
              $(".JC_Refresh").after('<a class="btn btn-show-link" style="background: #2b89ea; color: #fff; cursor: pointer">显示链接</a>');
              $(".btn-show-link").on("click", obj.showDownload);
          }
          else {
              setTimeout(obj.initHomePage, 500);
          }
      };

      obj.initSharePage = function () {
          if ($(".code-panel").length && option.isOptionActive(option.constant.ty189_page_verify)) {
              obj.initVerifyPage();
          }

          if (option.isOptionActive(option.constant.ty189_page_share)) {
              obj.initDownloadPage();
          }
      };

      obj.initVerifyPage = function () {
          obj.registerStoreSharePwd();

          obj.autoPaddingSharePwd();
      };

      obj.registerStoreSharePwd = function () {
          unsafeWindow.$(document).ajaxComplete(function (event, xhr, options) {
              var response = xhr.responseJSON;
              var sharePwd = null;
              if (options.url.indexOf("listShareDir.action") > 0) {
                  if (response instanceof Object && response.digest) {
                      var match = options.url.match(/accessCode=(\w+)/);
                      if (!match) {
                          return logger.warn("pwd share not match");
                      }

                      sharePwd = match[1];
                  }
                  else {
                      return logger.warn("pwd share not match");
                  }
              }
              else if (options.url.indexOf("shareFileVerifyPass.action") > 0) {
                  if (response instanceof Object && response.shareId && response.accessCode) {
                      sharePwd = response.accessCode;
                  }
                  else {
                      return logger.warn("pwd share not match");
                  }
              }
              else {
                  return logger.warn("not pwd request");
              }

              if (sharePwd == obj.verify_page.share_pwd) {
                  return logger.warn("pwd share not change");
              }

              var shareId = obj.getShareId();
              var shareLink = obj.getShareLink();
              shareLog.addShareLog(constant.source.ty189, shareId, sharePwd, shareLink);
          });
      };

      obj.autoPaddingSharePwd = function () {
          var shareId = obj.getShareId();
          shareLog.getShareLog(constant.source.ty189, shareId, function (record) {
              if (record instanceof Object && record.share_pwd) {
                  var sharePwd = record.share_pwd;
                  obj.verify_page.share_pwd = sharePwd;
                  $("#code_txt").val(sharePwd);
                  setting.showNotifySuccess() && obj.showTip(1, "[" + manifest.getTitle() + "] 回填访问码成功", 2000);

                  if (option.isOptionActive(option.constant.ty189_auto_jump)) {
                      setTimeout(function () {
                          unsafeWindow.$(".btn.visit").click();
                      }, 2000);
                  }
              }
              else {
                  setting.showNotifyFail() && obj.showTip(0, "[" + manifest.getTitle() + "] 没有访问码记录", 2000);
              }
          });
      };

      obj.showTip = function (code, msg, timeout) {
          var $element = $(".visit_error");
          if (code) {
              $element.safeHtml('<span style="color: green;">' + msg + '</span>');
          }
          else {
              $element.safeHtml('<span style="color: red;">' + msg + '</span>');
          }
          $element.show();
          setTimeout(function () {
              $element.hide();
          }, timeout);
      };

      obj.initDownloadPage = function () {
          $(".btn-download").after('<a class="btn btn-show-link" style="background: #2b89ea; cursor: pointer">显示链接</a>');
          $(".btn-show-link").on("click", obj.showDownload);

          if (unsafeWindow.fileId) {
              obj.getDownloadUrl($(".shareId").val(), unsafeWindow.fileId).then(function (downloadUrl) {
                  unsafeWindow.downloadUrl = downloadUrl + "filename=" + encodeURIComponent(unsafeWindow.fileName);
              });
          }
      };

      obj.showDownload = function () {
          var html = '<div style="padding: 20px; height: 410px; overflow-y: auto;">';
          var rowStyle = "margin:10px 0px; overflow:hidden; white-space:nowrap; text-overflow:ellipsis;";

          var fileIds = obj.getSelectedFileIds(),
              fileList = obj.getSelectedFileList();

          if (fileList.length > 1) {
              var packageUrl = obj.buildPackageUrl(fileIds, "打包下载.zip");
              html += '<p>压缩包</p>';
              html += '<p style="' + rowStyle + '"><a title="' + packageUrl + '" href="' + packageUrl + '" style="color: blue;">' + packageUrl + '</a></p>';
              html += '<p>&nbsp;</p>';
          }

          fileList.forEach(function (item, index) {
              var file = item.attributes;
              if (file.isFolder) {
                  file.downloadUrl = obj.buildPackageUrl(file.fileId, file.fileName + ".zip");
              }
              else {
                  file.downloadUrl = location.protocol + file.downloadUrl;
              }
              html += '<p>' + (++index) + '：' + (file.fileName ? file.fileName : file.fileId) + '</p>';
              html += '<p style="' + rowStyle + '"><a title="' + file.downloadUrl + '" href="' + file.downloadUrl + '" style="color: blue;">' + file.downloadUrl + '</a></p>';
          });

          html += '<div>';
          obj.showBox(html);
      };

      obj.showBox = function (body) {
          var template = '<div id="J_FileModal" class="treeBox-modal modal in" style="display:block"><div class="modal-dialog"><div class="modal-header"><a class="close">×</a><h3>文件下载</h3></div><div class="modal-body"></div></div></div>';
          if ($("#J_FileModal").length == 0) {
              $("body").append(template);
              $("#J_FileModal .close").on("click", function () {
                  $("#J_FileModal").hide();
              });
          }
          $("#J_FileModal").show();
          $("#J_FileModal .modal-body").safeHtml(body);
      };

      obj.buildPackageUrl = function (fileIds, fileName) {
          var downloadUrl = unsafeWindow.edrive.downloadUrl,
              sessionKey = unsafeWindow.edrive.sessionKey;
          fileName || (fileName = "");
          if (unsafeWindow._shareId) {
              return location.protocol + downloadUrl + "?sessionKey=" + sessionKey + "&fileIdS=" + fileIds + "&downloadType=3&shareId=" + unsafeWindow._shareId + "&filename=" + encodeURIComponent(fileName);
          }
          else {
              return location.protocol + downloadUrl + "?sessionKey=" + sessionKey + "&fileIdS=" + fileIds + "&downloadType=1&filename=" + encodeURIComponent(fileName);
          }
      };

      obj.buildDownloadUrl = function (shareId, fileDigest, fileName) {
          return "https://cloud.189.cn/downloadFile.action?fileStr=" + fileDigest + "&downloadType=3&shareId=" + shareId + "&filename=" + encodeURIComponent(fileName);
      };

      obj.getSelectedFileIds = function () {
          var fileIdList = [];
          var fileList = obj.getSelectedFileList();
          fileList.forEach(function (item) {
              fileIdList.push(item.attributes.fileId);
          });
          return fileIdList.join(",");
      };

      obj.getSelectedFileList = function () {
          var mainView = null, fileList = [];
          if (unsafeWindow.fileId) {
              fileList = [
                  {
                      attributes: unsafeWindow
                  }
              ];
          }
          else if (unsafeWindow._shareId) {
              mainView = unsafeWindow.appRouter.mainView;
              if (mainView instanceof Object && mainView.fileList) {
                  fileList = mainView.fileList;
                  if (fileList.selected().length) {
                      fileList = fileList.selected();
                  }
              }
              obj.processFileList(fileList, unsafeWindow._shareId);
          }
          else if (unsafeWindow.mainView) {
              mainView = unsafeWindow.mainView;
              if (mainView.fileListTabObj && mainView.fileListTabObj[mainView.options.fileId]) {
                  fileList = mainView.fileListTabObj[mainView.options.fileId].fileList.selected();
              }
              else if (mainView.getSelectedModels) {
                  fileList = mainView.getSelectedModels();
              }
          }

          var selectedFileList = [];
          fileList.forEach(function (item) {
              if (item.attributes.fileId > 0) {
                  selectedFileList.push(item);
              }
          });
          return selectedFileList;
      };

      obj.processFileList = function (fileList, shareId) {
          fileList.forEach(function (item) {
              if (item.attributes.isFolder !== true && item.attributes.fileIdDigest) {
                  item.attributes.downloadUrl = obj.buildDownloadUrl(shareId, item.attributes.fileIdDigest, item.attributes.fileName);
              }
          });
      };

      obj.getDownloadUrl = function (shareId, fileId) {
          return new Promise(function (resolve) {
              $.ajax({
                  url: "https://cloud.189.cn/v2/getFileDownloadUrl.action?shareId=" + shareId + "&fileId=" + fileId,
                  type: "get",
                  dateType: "text",
                  success: function (content) {
                      resolve(content);
                  },
                  error: function () {
                      resolve("");
                  }
              });
          });
      };

      obj.getShareId = function () {
          var url = obj.getShareLink();
          var match = url.match(/cloud\.189\.cn\/t\/([0-9a-z]+)/i);
          return match ? match[1] : null;
      };

      obj.getShareLink = function () {
          return router.getUrl();
      };

      return obj;
  });

  container.define("app_manage", ["meta", "unsafeWindow"], function (meta, unsafeWindow) {
      var obj = {};

      obj.run = function () {
          if (meta.existMeta("manage")) {
              unsafeWindow.OnePan = container;
              return true;
          }
      };

      return obj;
  });

  container.define("app", ["appRunner"], function (appRunner) {
      var obj = {};

      obj.run = function () {
          appRunner.run([
              {
                  name: "app_baidu",
                  matchs: [
                      "baidu.com"
                  ]
              },
              {
                  name: "app_weiyun",
                  matchs: [
                      "weiyun.com"
                  ]
              },
              {
                  name: "app_lanzous",
                  matchs: [
                      "lanzous.com",
                      "lanzoux.com"
                  ]
              },
              {
                  name: "app_189",
                  matchs: [
                      "cloud.189.cn"
                  ]
              },
              {
                  name: "app_manage",
                  matchs: [
                      "*"
                  ]
              }
          ]);
      };

      return obj;
  });

  /** lib **/
  container.define("$", [], function () {
      return window.$;
  });
  container.define("Snap", [], function () {
      if (typeof Snap != "undefined") {
          return Snap;
      }
      else {
          return window.Snap;
      }
  });
  container.define("DOMPurify", [], function () {
      if (typeof DOMPurify != "undefined") {
          return DOMPurify;
      }
      else {
          return window.DOMPurify;
      }
  });

  container.use(["gm", "core", "app"], function (gm, core, app) {
      gm.ready(function () {
          core.ready(app.run);
      });
  });
})();