import chromadb
import os

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "在文档知识库中搜索与用户问题相关的文档片段。当用户询问文档内容、项目信息、技术栈、运行方式等问题时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户的搜索问题，例如：项目用了什么技术栈？"
                    }
                },
                "required": ["query"]
            }
        }
    },
{
    "type": "function",
    "function": {
        "name": "list_documents",
        "description": "列出知识库中所有可用的文档文件。当用户询问有哪些文档、知识库里有什么文件等问题时使用。",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "计算简单数学表达式。当用户询问数学计算、算术运算等问题时使用，例如：1+1等于几、100乘以0.8",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "要计算的数学表达式，例如：1+1"
                }
            },
            "required": ["expression"]
        }
    }
}

]


def search_documents(query: str, n_results: int = 5) -> str:
    """
    在文档知识库中检索与问题相关的片段。

    参数:
        query: 用户的问题
        n_results: 返回的片段数量，默认 5

    返回:
        检索到的文档片段（字符串）
    """
    # 1. 连接向量库
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(name="documents")

    # 2. 检索
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    chunks = results['documents'][0]

    # 3. 拼接成字符串返回
    if not chunks:
        return "未找到相关文档片段。"

    return "\n\n".join(chunks)


def list_documents() -> str:
    """
    列出 data/ 目录下所有文档文件。

    返回:
        文档文件名列表（字符串）
    """
    data_dir = "data"
    if not os.path.exists(data_dir):
        return "文档目录不存在。"

    files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]

    if not files:
        return "知识库中暂无文档。"

    return "知识库中的文档：\n" + "\n".join(f"- {f}" for f in files)

def calculate(expression: str) -> str:
    """
    计算简单的数学表达式。

    参数:
        expression: 数学表达式，例如 "1+1"、"100*0.8"

    返回:
        计算结果（字符串）
    """
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        return "表达式包含不允许的字符，仅支持数字和 + - * / ( )。"

    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算失败：{e}"

if __name__ == "__main__":
    import json

    print("=== 工具描述 ===")
    print(json.dumps(TOOLS, ensure_ascii=False, indent=2))
    print()

    question = input("请输入测试问题：")
    result = search_documents(question)
    print("\n检索结果：")
    print(result)