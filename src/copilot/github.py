from openai import OpenAI

# 方式1：直接调用官方端点
client = OpenAI(
    base_url="https://api.githubcopilot.com",
    api_key="xxxxxxxxx"
)

# 方式2：先启动本地代理（需安装copilot-api并登录）
# client = OpenAI(base_url="http://127.0.0.1:3030/v1", api_key="copilot")

response = client.chat.completions.create(
    model="gpt-4o-copilot",
    messages=[{"role": "user", "content": "用Python实现一个快速排序算法"}]
)
print(response.choices[0].message.content)