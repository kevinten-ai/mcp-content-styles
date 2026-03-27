# 📰 公众号文章样例

**主题**: MCP 协议实战：5 分钟让 AI 调用本地工具
**模式**: rewrite
**预计字数**: ~1800 字

---

## MCP 协议实战：5 分钟让 AI 调用本地工具

上个月给 Claude Desktop 加了文件处理功能，踩了不少坑。这篇把核心流程和踩坑记录整理出来，照着做 5 分钟就能跑通。

---

### 01. 问题：重复对接的痛

做 AI 应用最烦的事情之一——同一个功能，不同平台要写不同的代码。

我之前的项目需要让 AI 操作本地文件。OpenAI 的 function calling 是一套格式，Claude 的 tool use 又是另一套，国内模型还各有各的写法。

**三套几乎一样的代码，维护起来崩溃。**

后来发现了 MCP（Model Context Protocol），简单说就是一个**让 AI 调用外部工具的统一接口**，类似 USB 接口统一了各种设备的连接方式——写一次 server，所有支持 MCP 的 client 都能用。

---

### 02. 技术选型：为什么选 MCP

选 MCP 之前也看过其他方案：

| 方案 | 优点 | 缺点 |
|------|------|------|
| 直接调平台 API | 灵活 | 每个平台写一遍 |
| LangChain Tools | 生态好 | 绑定 LangChain 框架 |
| **MCP** | **标准协议，跨平台** | **生态早期** |

最终选 MCP 的原因：**它是协议层的标准化，不绑定任何框架**。写一个 MCP server，Claude Desktop、Cursor、甚至自己的应用都能直接调用。

---

### 03. 实战：从零搭建文件操作 Server

**环境准备**

```bash
pip install mcp
```

> 需要 Python 3.10+，建议用虚拟环境。

**核心代码**

```python
from mcp.server.fastmcp import FastMCP

# 创建 MCP server 实例
app = FastMCP("file-tools")

@app.tool()
def read_file(path: str) -> str:
    """读取文件内容"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@app.tool()
def write_file(path: str, content: str) -> str:
    """写入文件"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"写入成功: {path}"

if __name__ == "__main__":
    app.run()
```

代码很简单：用 `@app.tool()` 装饰器注册工具函数，MCP SDK 自动处理协议层的事情。

**配置 Claude Desktop**

编辑配置文件，添加：

```json
{
  "mcpServers": {
    "file-tools": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

重启 Claude Desktop，在对话中说"帮我读取 /tmp/test.txt 的内容"——AI 就会自动调用你写的 `read_file` 工具。

---

### 04. 踩坑记录

跑通基本功能很快，但实际使用中遇到了几个问题。

**坑 1：Windows 编码问题**

默认读文件用的系统编码（Windows 是 GBK），中文文件直接报错。

解决：**所有文件操作显式指定 `encoding="utf-8"`**。这个看着简单，但第一次排查花了半小时，因为报错信息完全看不出是编码问题。

**坑 2：stdio 模式调试困难**

MCP 默认用 stdio 传输（标准输入输出），意味着 print 调试法用不了——print 的内容会被当成协议消息。

解决：用 **loguru 写日志到文件**，别往 stdout 输出任何东西。

```python
from loguru import logger
logger.add("server.log", rotation="10 MB")
```

**坑 3：安全问题**

裸跑的文件操作 server 能访问整个磁盘，生产环境绝对不行。

解决：加一个路径白名单：

```python
ALLOWED = ["/home/user/workspace"]

def check_path(path: str) -> bool:
    return any(path.startswith(p) for p in ALLOWED)
```

> 这个容易忽略，但一旦出问题就是安全事故。

---

### 05. 效果数据

用了一个月，对比一下前后差异：

| 指标 | 之前（直接调 API） | 之后（MCP） |
|------|-------------------|-------------|
| 对接代码量 | ~2000 行（3 套） | ~600 行（1 套） |
| 新增工具耗时 | 2-3 天 | 半天 |
| 支持的 client | 仅自己的应用 | Claude Desktop + Cursor + 自定义 |

**代码量减少 70%，最大的收益是不用重复劳动了。**

---

### 06. 写在最后

做完这个项目，我最大的感受是——AI 工具的价值不在于单个功能多强，而在于**连接能力**。

MCP 的方向是对的：与其让每个开发者重复造轮子，不如定义一个标准，让工具可以复用。但现阶段它还有明显的短板：文档分散、调试体验差、生态还在早期。

我的建议是：如果你在做需要 AI 调用本地工具的项目，现在就可以用 MCP。学习成本不高，半天能上手。但如果你对协议稳定性要求很高，可以再观望一两个版本。

完整代码已开源，GitHub 搜 `mcp-content-styles` 可以找到。

---

**推荐阅读**
- [MCP 官方文档](https://modelcontextprotocol.io)
- [FastMCP 库文档](https://github.com/jlowin/fastmcp)

---

如果觉得有帮助，欢迎点赞、在看。有问题评论区聊。
