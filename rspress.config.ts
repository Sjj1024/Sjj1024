import * as path from 'node:path'
import { defineConfig } from 'rspress/config'

export default defineConfig({
    root: path.join(__dirname, 'docs'),
    base: '/Sjj1024/',
    title: '1024小神',
    icon: '/xiaoshen.png',
    logo: {
        light: '/light-logo.png',
        dark: '/dark-logo.png',
    },
    themeConfig: {
        socialLinks: [
            {
                icon: 'bilibili',
                mode: 'link',
                content: 'https://space.bilibili.com/405719127',
            },
            {
                icon: 'juejin',
                mode: 'link',
                content: 'https://juejin.cn/user/70007368988926',
            },
            {
                icon: 'github',
                mode: 'link',
                content: 'https://github.com/Sjj1024',
            },
        ],
    },
})
