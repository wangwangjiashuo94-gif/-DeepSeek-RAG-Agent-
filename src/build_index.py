from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

# 1. 读取并切块
with open("data/document.txt", "r", encoding="utf-8") as f:
    text = f.read()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)
chunks = splitter.split_text(text)

# 2. 创建 Chroma 客户端（数据存在 chroma_db 文件夹）
client = chromadb.PersistentClient(path="chroma_db")

# 3. 创建或获取一个 collection（类似数据库里的一张表）
collection = client.get_or_create_collection(name="documents")

# 4. 存入文档块
# ids：每块的唯一编号，不能重复
# documents：文本内容
collection.add(
    documents=chunks,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

# 5. 打印结果
print(f"文档切块数：{len(chunks)}")
print(f"向量库中存储数：{collection.count()}")
print("索引构建完成！")