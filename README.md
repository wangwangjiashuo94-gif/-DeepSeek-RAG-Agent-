# 文档问答 RAG 系统

基于 DeepSeek + Chroma 的 RAG 文档问答系统，并支持 Function Calling Agent 多工具调用与多轮对话。

支持将本地文档切块、向量化存储，并根据用户问题检索相关片段后生成回答。

---

 技术栈

- Python 3.14
- DeepSeek API（大模型生成）
- Chroma（向量数据库）
- LangChain Text Splitters（文档切块）
- OpenAI SDK（兼容 DeepSeek 接口）
- python-dotenv（环境变量管理）
- DeepSeek Function Calling（Agent 工具调用）

---

项目结构

doc-qa-agent/

├── data/                  # 存放待问答文档

│   └── document.txt

├── src/

│   ├── chunk_[document.py](http://document.py)  # 文档切块测试脚本

│   ├── build_[index.py](http://index.py)     # 构建向量索引

│   ├── [search.py](http://search.py)          # 检索测试脚本

│   ├── rag_[qa.py](http://qa.py)          # RAG 问答主入口

│   ├──[tools.py](http://tools.py)              #工具函数 + 工具描述

│   └──[agent.py](http://agent.py)             #agent主入口

├── chroma_db/             # 向量库数据（运行 build_[index.py](http://index.py) 后自动生成）

├── venv/                  # Python 虚拟环境

├── [qa.py](http://qa.py)                  # 旧版 Demo（整篇文档直接问答，对比用）

├── .env                   # API Key 配置（需自行创建）

├── .gitignore

├── requirements.txt

└── [README.md](http://README.md)

---

快速开始

1. 克隆项目并进入目录

cd doc-qa-agent

2.创建并激活虚拟环境

py -3.14 -m venv venv

venv\Scripts\activate

3.安装依赖

pip install -r requirements.txt

4.配置 API Key

在项目根目录创建 .env 文件，写入：

DEEPSEEK_API_KEY=sk-你的key

5.准备文档

将待问答的文档放入 data/ 目录（当前支持 .txt）。

6.构建向量索引

python src/build_[index.py](http://index.py)

文档内容有变更时，需要重新运行此命令。

1. Agent 问答（推荐）：
  python src/[agent.py](http://agent.py)
   支持连续对话，输入 quit 退出。

---

RAG 工作流程

文档 → 切块（chunk）→ 向量化（embedding）→ 存入 Chroma

提问 → 检索相关文档块 → 拼接上下文 → DeepSeek 生成回答

与旧版 [qa.py](http://qa.py) 的区别：

- [qa.py](http://qa.py)：整篇文档塞入 prompt，文档长了会超限、费 token
- rag_[qa.py](http://qa.py)：只检索最相关的 5 个片段，更精准、更省钱

Agent工作流程

用户提问 → DeepSeek 决定调用哪个工具 → 执行工具 → 结果送回模型 → 生成回答

（如需可继续多轮工具调用，直到给出最终答案）

可用工具：

- search_documents：检索文档内容
- list_documents：列出知识库文件
- calculate：简单数学计算

---

当前进度

**已完成（阶段二）：**

- 工具函数封装（`tools.py`）
- DeepSeek Function Calling
- 3 个工具：检索 / 列举 / 计算
- 多轮工具调用循环
- 多轮对话记忆

**后续计划（阶段三）：**

- Web UI（Streamlit）
- 中文 Embedding 优化
- Docker 部署
- 更多工具（如文档摘要）

---

**阶段二：Agent 规划**

一句话说 RAG 和 Agent 的区别：rag所有流程写死的不管怎么问他，他处理问题的流程都固定，agent会灵活变通，根据需求处理事情返回结果

引入工具：**Function Calling，吧RAG打包为工具**

为什么要在 RAG 之上做 Agent：RAG不适于现在的市场，不够智能，不会自己选择工具

常见问题

**Q：运行 build_[index.py](http://index.py) 时下载模型很慢？**

A：首次运行 Chroma 会自动下载 Embedding 模型，等待即可。

**Q：换了文档后问答内容没更新？**

A：需要重新运行 python src/build_[index.py](http://index.py) 重建索引。

**Q：为什么要用虚拟环境？**

A：项目依赖 Python 3.14，虚拟环境隔离不同项目的 Python 版本和包。

---

 许可证

MIT