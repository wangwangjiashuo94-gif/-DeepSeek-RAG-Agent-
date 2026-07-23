from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. 读取文档
with open("data/document.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 2. 配置切块器
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,      # 每块大约 200 个字符
    chunk_overlap=50     # 相邻块之间重叠 50 个字符，避免一句话被截断
)

# 3. 执行切块
chunks = splitter.split_text(text)

# 4. 打印结果
print(f"文档总长度：{len(text)} 字符")
print(f"切分块数：{len(chunks)}")
print("-" * 40)

for i, chunk in enumerate(chunks):
    print(f"\n【第 {i + 1} 块】长度：{len(chunk)} 字符")
    print(chunk)
    print("-" * 40)