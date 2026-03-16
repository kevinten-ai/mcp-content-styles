# 🚀 快速开始指南

本指南帮助你在 5 分钟内上手 MCP Content Styles。

## 📋 前提条件

- Python 3.10+
- Claude Desktop 或其他 MCP 客户端

## ⚡ 一键安装

```bash
# 1. 克隆仓库
git clone https://github.com/kevinten-ai/mcp-content-styles.git
cd mcp-content-styles

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -e .

# 4. 验证安装
python -c "from mcp_content_styles.skill_manager import SkillManager; print('✅ 安装成功')"
```

## 🔧 配置 Claude Desktop

### macOS

```bash
# 创建/编辑配置文件
mkdir -p ~/Library/Application\ Support/Claude
cat > ~/Library/Application\ Support/Claude/claude_desktop_config.json << 'EOF'
{
  "mcpServers": {
    "content-styles": {
      "command": "python",
      "args": ["-m", "mcp_content_styles.main"],
      "cwd": "FULL_PATH_TO/mcp-content-styles"
    }
  }
}
EOF
```

### Windows

```powershell
# 创建配置文件
$claudeDir = "$env:APPDATA\Claude"
New-Item -ItemType Directory -Force -Path $claudeDir

@'
{
  "mcpServers": {
    "content-styles": {
      "command": "python",
      "args": ["-m", "mcp_content_styles.main"],
      "cwd": "C:\\full\\path\\to\\mcp-content-styles"
    }
  }
}
'@ | Set-Content "$claudeDir\claude_desktop_config.json"
```

### Linux

```bash
mkdir -p ~/.config/claude
cat > ~/.config/claude/claude_desktop_config.json << 'EOF'
{
  "mcpServers": {
    "content-styles": {
      "command": "python",
      "args": ["-m", "mcp_content_styles.main"],
      "cwd": "/full/path/to/mcp-content-styles"
    }
  }
}
EOF
```

**⚠️ 注意**: 将 `FULL_PATH_TO` 替换为实际的绝对路径。

## 🎯 第一步：查看支持的平台

在 Claude Desktop 中，你可以直接询问：

```
你能列出 content-styles 支持的所有平台吗？
```

或者使用工具：

```python
platforms = list_platforms()
print(platforms)
```

**预期输出：**
```
📚 zhihu_article - 知乎专栏文章风格 - 技术深度解析
📰 wechat_article - 微信公众号文章风格 - AI工程化实践
📕 xiaohongshu_note - 小红书笔记风格 - AI工具推荐
🐦 weibo_post - 微博博文风格 - 快速分享
🎵 douyin_script - 抖音视频脚本风格 - AI工具演示
```

## 📝 第二步：转换内容

### 示例：小红书风格

**你的原始 Markdown：**

```markdown
## Claude Code 使用体验

最近体验了 Claude Code，真的很强大！

主要特点：
- 智能代码补全
- 自然语言交互
- 项目级理解
```

**在 Claude 中：**

```
帮我把上面的内容转换成小红书风格的笔记，主题是"Claude Code AI编程神器"
```

Claude 会自动调用 `get_platform_prompt` 工具，然后生成小红书风格的内容：

```markdown
## 💡 发现AI编程神器！Claude Code绝了！

**宝子们！** 今天必须给你们安利一个超厉害的AI工具！

### 😭 以前的痛
写代码总是卡顿，效率低...

### ✨ 终于找到救星
Claude Code 真的太香了！

- ⚡ 智能代码补全，秒懂你的意图
- 💬 自然语言交互，说人话就能写代码
- 🧠 项目级理解，整个 codebase 都懂

### 🔥 实测效果
以前写功能要2小时，现在20分钟搞定！

**你们用过吗？评论区聊聊！** 👇

#ClaudeCode #AI工具 #编程效率 #程序员必备 #效率神器
```

## 🔄 第三步：批量转换

如果你有内容需要发布到多个平台：

```
帮我把这篇文章转换成：
1. 知乎风格（技术深度）
2. 公众号风格（AI工程化）
3. 小红书风格（工具推荐）

原始内容：
---
[PASTE YOUR MARKDOWN HERE]
---
```

Claude 会调用 `convert_content` 工具，为每个平台生成专属 prompt，然后生成适配的内容。

## 🎨 第四步：生成配图

结合 `mcp-image` MCP 使用：

```python
# 1. 生成内容
content = get_platform_prompt(
    platform="xiaohongshu",
    mode="format",
    topic="AI工具推荐",
    original_content=my_markdown
)

# 2. 生成配图
image_prompt = f"小红书风格封面图，主题是：{topic}，内容关于AI编程工具"
image = mcp_image.generate(image_prompt)

# 3. 输出最终内容
print("内容：", content)
print("配图：", image)
```

## 📊 模式对比

| 模式 | 适用场景 | 输出特点 |
|------|----------|----------|
| **format** | 内容完整，需排版 | 保持结构，调整格式 |
| **rewrite** | 需重新组织，求爆款 | 智能重写，优化传播 |

### Format 模式示例

**输入：**
```markdown
## AI工具介绍

Claude Code 是一个AI编程助手。
特点：
1. 代码补全
2. 自然语言
3. 项目理解
```

**输出：** 保持原有结构，添加小红书格式（Emoji、短段落、hashtags）

### Rewrite 模式示例

**输入：** 同上

**输出：** 重新组织为"痛点-解决方案-效果-总结"结构，使用更吸引人的表达

## 🛠️ 故障排除

### 问题 1：MCP 服务器未显示

**症状**：Claude Desktop 中没有 content-styles 工具

**解决**：
1. 检查配置文件路径是否正确
2. 确认 `cwd` 是绝对路径
3. 重启 Claude Desktop
4. 检查日志：`~/Library/Logs/Claude/mcp*.log`

### 问题 2：导入错误

**症状**：`ModuleNotFoundError: No module named 'mcp_content_styles'`

**解决**：
```bash
cd /path/to/mcp-content-styles
pip install -e .
```

### 问题 3：技能未找到

**症状**：`Error: Skill 'xxx' not found`

**解决**：
1. 检查技能名称拼写
2. 查看可用技能：`list_platforms()`
3. 检查技能文件是否存在：`ls src/mcp_content_styles/skills/`

## 📚 下一步

- 阅读完整 [README.md](../README.md)
- 查看 [使用示例](../examples/usage_example.py)
- 了解 [API 文档](API.md)（待完善）
- 贡献新的平台模板

## 💡 提示

1. **使用绝对路径**：配置文件中的 `cwd` 必须是绝对路径
2. **虚拟环境**：建议使用虚拟环境避免依赖冲突
3. **日志调试**：查看 Claude Desktop 日志排查问题
4. **模板定制**：直接编辑 `src/mcp_content_styles/skills/*.md` 文件定制模板

---

**🎉 恭喜！你已完成快速开始配置！**

开始使用 MCP Content Styles 创作你的内容吧！
