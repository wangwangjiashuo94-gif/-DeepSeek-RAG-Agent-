import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS, search_documents, list_documents, calculate

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 1. 初始化对话（system 只设置一次）
messages = [
    {
        "role": "system",
        "content": """你是一个智能文档助手，可以使用工具来帮助用户。

规则：
1. 当工具返回结果后，请直接根据结果回答用户，不要只说「让我再搜索」而不行动
2. 如果工具结果已足够，立即整理并回答，不要重复调用相同工具
3. 文档相关问题用 search_documents，列举文件用 list_documents，数学计算用 calculate
4. 如果工具结果中没有相关信息，明确告诉用户「未找到相关信息」"""
    }
]

max_rounds = 5

# 2. 外层循环：支持多轮对话
while True:
    question = input("\n请输入你的问题（输入 quit 退出）：")

    if question.strip().lower() in ["quit", "exit", "q"]:
        print("再见！")
        break

    messages.append({"role": "user", "content": question})

    # 3. 内层循环：多轮工具调用
    for round_num in range(max_rounds):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=TOOLS
        )

        message = response.choices[0].message

        if not message.tool_calls:
            print("\n回答：")
            print(message.content)
            messages.append({"role": "assistant", "content": message.content})
            break

        print(f"\n[Agent 第 {round_num + 1} 轮] 模型决定调用工具...")
        messages.append(message)

        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"[Agent] 调用 {function_name}，参数：{arguments}")

            if function_name == "search_documents":
                tool_result = search_documents(arguments["query"])
            elif function_name == "list_documents":
                tool_result = list_documents()
            elif function_name == "calculate":
                tool_result = calculate(arguments["expression"])
            else:
                tool_result = "未知工具"

            print(f"[Agent] 工具返回了 {len(tool_result)} 个字符")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })
    else:
        print("\n已达到最大调用轮数，请简化问题后重试。")