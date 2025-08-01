const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    //mode 指打包模式
    //development 指开发模式，代码未压缩
    //production 指产品模式，代码压缩
    mode: 'production',    //development and production

    //entry 指明入口文件，webpack 会从这个文件开始连接所有的依赖。
    entry: {
        './background.js': __dirname + '/background.js',
        './content.js': __dirname + '/content.js',
        './static/js/popup.js': __dirname + '/static/js/popup.js',
        './static/js/gtag.js': __dirname + '/static/js/gtag.js',
        './static/js/jquery.js': __dirname + '/static/js/jquery.js',
        './static/js/utils.js': __dirname + '/static/js/utils.js',
    },

    //output 指明出口文件， 即打包后的文件存放的位置
    output: {
        path: __dirname + '/dist',
        // filename: '[name]_bundle_[hash].js',
        filename: '[name]',
    },

    //文件加载器 loader
    //loader 让 webpack 能够去处理那些非 JavaScript 文件（webpack 自身只理解 JavaScript）
// loader设置
//     module: {
//         rules: [
//             {
//                 test: /\.(css|sass|scss)$/,
//                 loaders: ['style-loader', 'css-loader']
//             },
//             {
//                 test: /\.(jsx|js)$/,
//                 use: [{
//                     loader: 'babel-loader',
//                     options: {
//                         presets: [
//                             'env', 'react', 'stage-0'
//                         ]
//                     }
//                 }]
//             },
//             {
//                 test: /\.xml$/,
//                 loaders: ['xml-loader']
//             },
//             {
//                 test: /\.(png|svg|jpg|gif|mp4)$/,
//                 use: [{
//                     loader: 'file-loader',
//                     options: {
//                         outputPath: './img',
//                         publicPath: './img'
//                     }
//                 }]
//             }
//         ]
//     },
//
    //插件
    plugins: [
        new HtmlWebpackPlugin({ //输出html文件1
            title: '首页',   //生成html文件的标题
            favicon: './favicon.png',   //生成html文件的favicon的路径
            filename: 'first.html',     //生成html文件的文件名，默认是index.html
            template: 'first.html',     //本地html文件模板的地址
            hash: true,
            chunks: ['./js/first']
        }),
        new HtmlWebpackPlugin({ //输出html文件2
            title: '导航页',
            favicon: './favicon.png',
            filename: 'second.html',
            template: 'second.html',
            hash: true,
            chunks: ['./js/second']
        })
    ]
}
