import chromadb

# 1. 连接已有的数据库
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="documents")

# 2. 让用户输入问题
query = input("请输入你的问题：")

# 3. 检索最相关的 2 个文档块
results = collection.query(
    query_texts=[query],
    n_results=2
)

# 4. 打印检索结果
print(f"\n问题：{query}")
print(f"找到 {len(results['documents'][0])} 个相关片段：")
print("=" * 50)

for i, doc in enumerate(results['documents'][0]):
    print(f"\n【相关片段 {i + 1}】")
    print(doc)
    print("-" * 50)