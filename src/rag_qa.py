import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()

# 1. 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 2. 连接向量库
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")

# 3. 用户提问
question = input("请输入你的问题：")

# 4. 检索相关文档块（取 5 块）
results = collection.query(
    query_texts=[question],
    n_results=5
)
retrieved_chunks = results['documents'][0]

# 5. 拼成上下文
context = "\n\n".join(retrieved_chunks)

# 6. 调用 DeepSeek 生成回答
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "system",
            "content": f"你是一个文档问答助手。请仅根据下面提供的文档片段回答用户问题，不要编造文档中没有的信息。如果文档中没有相关信息，请明确说「文档中未找到相关信息」。\n\n文档片段：\n{context}"
        },
        {
            "role": "user",
            "content": question
        }
    ]
)

# 7. 输出回答
print("\n回答：")
print(response.choices[0].message.content)

print("\n--- 参考来源 ---")
for i, chunk in enumerate(retrieved_chunks):
    print(f"\n[片段 {i + 1}] {chunk[:80]}...")