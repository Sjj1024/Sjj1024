// 解析查询参数

const url = new URL(window.location.href)
const params = url.searchParams
const name = params.get('name')
const age = params.get('age')

console.log(name, age)
