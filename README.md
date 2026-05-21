# 🤖 AI 智能助手

基于 **Streamlit** 和 **DeepSeek API** 构建的智能对话机器人，支持多会话管理、个性化助手设置（昵称 + 性格），并具备流式输出与对话保存功能。

---

## ✨ 功能特点

- 💬 **智能对话**：调用 DeepSeek 大模型，支持流式输出，响应更自然。
- 🧠 **个性化助手**：可自定义助手的昵称和性格特征（如“广东本地人”）。
- 📁 **会话管理**：
  - 自动保存对话记录
  - 支持创建、切换、删除多个会话
  - 会话以 JSON 格式存储在本地 `sessions/` 目录
- 🎨 **界面友好**：基于 Streamlit 构建，操作简单，布局清晰。

---

## 🛠️ 技术栈

- Python 3.8+
- Streamlit
- OpenAI SDK（兼容 DeepSeek API）
- JSON 文件存储

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourname/ai-partner.git
cd ai-partner
pip install streamlit openai
export DEEPSEEK_API_KEY="your-deepseek-api-key"
streamlit run AI_partner.py
```
.
├── AI_partner.py          # 主程序
├── sessions/              # 会话存储目录（自动生成）
│   └── 20250321120000.json
└── README.md
🧪 使用说明
开始对话：在输入框中输入问题，助手会实时回复。

切换助手：在侧边栏修改"助手名称"或"助手性格"，会立即生效。

会话管理：

点击"新建会话"可开启新对话。

侧边栏显示历史会话列表，可点击加载或删除。

自动保存：每次对话后会自动保存当前会话。

⚙️ 高级配置
模型选择：当前使用 deepseek-v4-pro，可在代码中修改。

流式输出：已启用，支持逐字显示。

思考模式：已启用 thinking 参数，可展示模型推理过程（如支持）。

❗ 注意事项
请确保网络可访问 DeepSeek API。

首次运行会自动创建 sessions/ 目录。

删除会话会同时删除对应的 JSON 文件，请谨慎操作。

📌 后续优化建议
支持更多大模型（如 GPT、Claude）

增加对话导出功能（TXT / Markdown）

支持多语言界面

增加对话搜索功能

📄 许可证
MIT License

🙏 致谢
Streamlit

DeepSeek
