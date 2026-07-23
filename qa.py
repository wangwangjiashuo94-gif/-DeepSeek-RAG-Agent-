import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

# 1. 配置API客户端（DeepSeek的接口兼容OpenAI格式）
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 2. 读取本地文档内容
with open("data/document.txt", "r", encoding="utf-8") as f:
    document_content = f.read()



 

# 3. 让用户输入问题
question = input("请输入你想问这份文档的问题：")

# 4. 把文档内容和问题一起交给大模型，要求它基于文档内容回答
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "system",
            "content": f"你是一个文档问答助手，请仅根据下面提供的文档内容回答用户问题，不要编造文档中没有的信息。\n\n文档内容：\n{document_content}"
        },
        {
            "role": "user",
            "content": question
        }
    ]
)

# 5. 输出回答
print("\n回答：")
print(response.choices[0].message.content)