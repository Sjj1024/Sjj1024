"""
agent.py - 极简 AI Agent 原型（可直接运行）
说明：
- LLM 部分用一个非常简单的"规则回答器"模拟，实际接入 LLM 时替换 LLMInterface.generate(...)
- 包含组件：LLM 抽象、大脑(解析/决策)、规划器、工具注册器、内存、执行器
"""

from typing import Any, Dict, List, Callable
import time


# -----------------------------
# Memory（非常轻量）
# -----------------------------
class Memory:
    def __init__(self):
        self.short = {}  # 当前会话上下文
        self.long = {}  # 长期偏好/联系人等

    def get_short(self, k, default=None):
        return self.short.get(k, default)

    def set_short(self, k, v):
        self.short[k] = v

    def get_long(self, k, default=None):
        return self.long.get(k, default)

    def set_long(self, k, v):
        self.long[k] = v


# -----------------------------
# LLM 抽象（替换点）
# -----------------------------
class LLMInterface:
    def generate(self, prompt: str) -> str:
        """
        这里给出一个非常简单的规则式模拟回答器。
        真实使用时：替换为 OpenAI/其它模型的调用代码，返回 model 文本。
        """
        # 极简解析示例：识别是否需要判断"下雨"
        if "是否下雨" in prompt or "下雨" in prompt:
            return "请先查询天气；如果有雨，请生成提醒并发送给目标联系人。"
        if "生成提醒" in prompt:
            return "请提醒小王：明天北京有雨，请带伞。"
        return "我理解了。"


# -----------------------------
# 工具注册与模拟工具
# -----------------------------
class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, fn: Callable[..., Any]):
        self.tools[name] = fn

    def call(self, name: str, *args, **kwargs):
        if name not in self.tools:
            raise ValueError(f"工具未注册: {name}")
        return self.tools[name](*args, **kwargs)


# 模拟工具：天气查询（真实情况会调用天气 API）
def mock_weather_api(city: str, date: str) -> Dict[str, Any]:
    # 简单规则：如果 city 包含 "北京" 且 date 包含 "明天"，返回下雨示例
    if "北京" in city and "明天" in date:
        return {"city": city, "date": date, "cond": "雨", "precip_mm": 5}
    return {"city": city, "date": date, "cond": "晴", "precip_mm": 0}


# 模拟工具：发送消息（真实情况会调用短信/邮件/企业微信等）
def mock_send_message(contact: str, message: str) -> bool:
    print(f"[发送消息] to={contact} message={message}")
    return True


# 模拟工具：简单搜索（示意）
def mock_search(query: str) -> str:
    return f"模拟搜索结果：关于 `{query}` 的信息摘要。"


# -----------------------------
# Planner / Executor
# -----------------------------
class SimplePlanner:
    def plan(self, goal: str) -> List[Dict[str, Any]]:
        """
        将目标拆解为步骤列表（非常简化的实现）
        每一步包含：action(工具名或内部动作)、params
        """
        steps = []
        # 例：若提示包含"天气"，生成两个步骤：查天气、判断并可能发提醒
        if "天气" in goal or "下雨" in goal:
            steps.append({"action": "query_weather", "params": {"city": "北京", "date": "明天"}})
            steps.append({"action": "decide_and_notify", "params": {"contact_name": "小王"}})
        else:
            steps.append({"action": "search", "params": {"query": goal}})
        return steps


class Executor:
    def __init__(self, tools: ToolRegistry, memory: Memory, llm: LLMInterface):
        self.tools = tools
        self.memory = memory
        self.llm = llm

    def run_step(self, step: Dict[str, Any]):
        action = step["action"]
        params = step.get("params", {})
        if action == "query_weather":
            res = self.tools.call("weather", params["city"], params["date"])
            self.memory.set_short("last_weather", res)
            return res
        if action == "decide_and_notify":
            weather = self.memory.get_short("last_weather", {})
            # 简单规则决策
            if weather.get("cond") == "雨":
                # 让 LLM 生成提醒文本（示例）
                prompt = f"基于天气信息：{weather}，生成一条发给{params['contact_name']}的提醒。"
                reminder = self.llm.generate(prompt)
                # 从长期记忆中获取联系方式
                contact = self.memory.get_long(params["contact_name"]) or "13800000000"
                ok = self.tools.call("send_message", contact, reminder)
                return {"notified": ok, "message": reminder}
            else:
                return {"notified": False, "reason": "天气晴朗"}
        if action == "search":
            return self.tools.call("search", params["query"])
        raise ValueError(f"未知动作: {action}")


# -----------------------------
# Agent 本体
# -----------------------------
class SimpleAgent:
    def __init__(self):
        self.memory = Memory()
        self.tools = ToolRegistry()
        self.llm = LLMInterface()
        self.planner = SimplePlanner()
        self.executor = Executor(self.tools, self.memory, self.llm)
        # 注册默认工具
        self.tools.register("weather", mock_weather_api)
        self.tools.register("send_message", mock_send_message)
        self.tools.register("search", mock_search)
        # 假设长期记忆里存了小王的联系方式
        self.memory.set_long("小王", "13911112222")

    def handle(self, user_prompt: str):
        # 1) 大脑解析（用 LLM 抽象）
        intent = self.llm.generate(user_prompt)
        # 2) 规划
        steps = self.planner.plan(user_prompt)
        # 3) 逐步执行
        results = []
        for step in steps:
            r = self.executor.run_step(step)
            results.append({"step": step, "result": r})
        # 4) 输出合并
        return {"intent": intent, "steps": results}


# -----------------------------
# 运行示例
# -----------------------------
if __name__ == "__main__":
    agent = SimpleAgent()
    task = "查一下明天北京的天气，如果下雨，帮我写个提醒并发给小王。"
    out = agent.handle(task)
    import json

    print(json.dumps(out, ensure_ascii=False, indent=2))
