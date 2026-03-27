# 🐦 X/Twitter 推文样例

**主题**: MCP 协议 - AI 工具集成实战
**模式**: rewrite (Thread)

---

1/ MCP protocol 让我把 3 套 AI 对接代码减到 1 套。

折腾了一个月，分享一下真实体验。

🧵

2/ 问题：同一个工具要分别对接 OpenAI / Claude / 国内模型。

每个平台 SDK 不一样，function calling 的格式也不同。写了三遍几乎一样的代码。

3/ MCP (Model Context Protocol) 的思路：

定义一套标准接口，让 AI 调用本地工具。写一次 server，所有支持 MCP 的 client 都能用。

类似 LSP 对编辑器做的事情。

4/ 实际效果：

- 对接代码从 ~2000 行 → ~600 行
- Claude Desktop + Cursor 同时可用
- Python 的 FastMCP 库半天就能跑通第一个工具

5/ 但也有坑：

- 文档分散，官方 + SDK + 社区散落各处
- stdio 模式调试体验差，序列化问题排查了一下午
- 生态早期，现成 server 不多

6/ 适合的场景：
✅ 需要让 AI 调用本地工具
✅ 同时对接多个 AI 平台
✅ 做 AI 工具自动化

不适合：只用一个平台、对协议稳定性要求高

7/ 代码开源了，link in bio。

方向是对的，但现阶段需要折腾能力。

你们在用什么方案做 AI 工具集成？

#MCP #buildinpublic #AI
