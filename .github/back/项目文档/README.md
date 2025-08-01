# PPC-WEB 分支：v1.1

## 启动步骤

# 安装依赖

npm install

# 启动服务 localhost:8028

npm run dev

# 打包压缩

npm run build

# 打包-分析包

npm run build --report

### git提交规范

* feat：新建 feature
* fix: 修复 bug
* docs: 仅仅修改了文档，比如 README, CHANGELOG, CONTRIBUTE等等
* style: 仅仅修改了空格、格式缩进、逗号等等，不改变代码逻辑
* refactor: 代码重构，没有加新功能或者修复 bug
* perf: 优化相关，比如提升性能、体验
* test: 测试用例，包括单元测试、集成测试等
* chore: 改变构建流程、或者增加依赖库、工具等
* revert: 回滚到上一个版本


## vscode 配置


```
{
  "editor.fontSize": 16,
  "[javascript]": {
    "editor.defaultFormatter": "vscode.typescript-language-features",
  },
  "editor.minimap.enabled": true,
  "js/ts.implicitProjectConfig.experimentalDecorators": true,
  "editor.tabSize": 2,
  "explorer.confirmDelete": false,
  "javascript.updateImportsOnFileMove.enabled": "never",
  "[json]": {
    "editor.quickSuggestions": {
      "strings": true
    },
    "editor.suggest.insertMode": "replace"
  },
  "workbench.colorTheme": "Atom One Dark",
  "workbench.iconTheme": "material-icon-theme",
  "workbench.preferredDarkColorTheme": "Solarized Light",
  "workbench.preferredHighContrastColorTheme": "Default Dark+",
  "material-icon-theme.activeIconPack": "react",
  "material-icon-theme.folders.theme": "classic",
  "material-icon-theme.hidesExplorerArrows": true,
  "git.confirmSync": false,
  "vetur.validation.template": false,
  "security.workspace.trust.untrustedFiles": "open",
  "tslint.trace.server": "messages",
  "tslint.typeCheck": true,
  "volar.codeLens.references": false,
  "[vue]": {
    "editor.defaultFormatter": "octref.vetur",
  },
  "[css]": {
    "editor.defaultFormatter": "michelemelluso.code-beautifier"
  },
  "json.schemas": [],
  // 代码格式化
  // vscode默认启用了根据文件类型自动设置tabsize的选项
  "editor.detectIndentation": false,
  // 重新设定tabsize
  "vetur.format.options.tabSize": 2,
  // 添加 vue 支持
  "eslint.validate": [
    "javascript",
    "html",
    "vue"
  ],
  //  去掉代码结尾的分号
  "prettier.semi": false,
  "prettier.tabWidth": 4,
  //  使用单引号替代双引号
  "prettier.singleQuote": true,
  //  让函数(名)和后面的括号之间加个空格
  "javascript.format.insertSpaceBeforeFunctionParenthesis": false,
  //  这个按用户自身习惯选择
  "vetur.format.defaultFormatter.html": "js-beautify-html",
  // "vetur.format.defaultFormatter.html": "prettier",
  "vetur.format.defaultFormatterOptions": {
    // vue组件中html代码格式化样式
    "js-beautify-html": {
      // 对属性进行换行。
      // - auto: 仅在超出行长度时才对属性进行换行。
      // - force: 对除第一个属性外的其他每个属性进行换行。
      // - force-aligned: 对除第一个属性外的其他每个属性进行换行，并保持对齐。
      // - force-expand-multiline: 对每个属性进行换行。
      // - aligned-multiple: 当超出折行长度时，将属性进行垂直对齐。
      "wrap_attributes": "force-expand-multiline",
      "indent_size": 2,
    },
    "prettyhtml": {
      "wrapAttributes": true
    },
    "prettier": {
      "semi": false,
      "singleQuote": true,
      "trailingComma": "none"
    }
  },
  // 每次保存的时候将代码按eslint格式进行修复
  "editor.codeActionsOnSave": {
    "source.fixAll": true,
  },
  // 代码是否按屏幕宽度换行
  "editor.wordWrap": "on",
}
```
