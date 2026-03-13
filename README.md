# MCP Content Styles

MCP server providing platform-specific content creation prompts.

## Supported Platforms

| Platform | Content Types | Style |
|----------|--------------|-------|
| 知乎 (zhihu) | article, answer | 技术深度 |
| 微信公众号 (wechat) | article | AI工程化 |
| 小红书 (xiaohongshu) | note, image | 工具推荐 |
| 微博 (weibo) | post | 快速分享 |
| 抖音 (douyin) | script | 视频脚本 |

## Installation

```bash
pip install -e .
```

## Usage

### Run the MCP Server

```bash
# Method 1: Direct run
python -m mcp_content_styles.main

# Method 2: Entry point
mcp-content-styles
```

### MCP Tools

#### 1. `get_platform_prompt`

Get platform-specific prompt template.

**Parameters:**
- `platform` (str): Platform name
- `content_type` (str): Content type
- `mode` (str): "format" or "rewrite"
- `topic` (str): Topic for rewrite mode
- `original_content` (str): Original markdown

**Example:**

```python
prompt = get_platform_prompt(
    platform="xiaohongshu",
    content_type="note",
    mode="format",
    original_content="## AI工具推荐\n\n我测试了50个工具..."
)
```

#### 2. `list_platforms`

List all available platforms.

```python
platforms = list_platforms()
```

#### 3. `convert_content`

Convert markdown to platform format with instructions.

```python
result = convert_content(
    markdown_content="## My Article...",
    platform="zhihu",
    mode="format"
)
```

#### 4. `get_skill_content`

Get raw skill template.

```python
template = get_skill_content("zhihu_article")
```

## Complete Workflow

```python
# 1. Get platform prompt
prompt = get_platform_prompt(
    platform="xiaohongshu",
    content_type="note",
    mode="format",
    original_content=my_markdown
)

# 2. Use with LLM to generate content
content = llm.generate(prompt)

# 3. Generate media with other MCPs
image = mcp_image.generate(f"xiaohongshu style: {content}")

# 4. Publish
mcp_xiaongshu.publish(content, image)
```

## Skill Templates

Each platform has a corresponding Markdown skill template in `src/mcp_content_styles/skills/`:

| Skill File | Platform | Description |
|------------|----------|-------------|
| `zhihu_article.md` | 知乎 | 技术深度文章 |
| `wechat_article.md` | 微信公众号 | AI工程化实践 |
| `xiaohongshu_note.md` | 小红书 | 工具推荐笔记 |
| `weibo_post.md` | 微博 | 快速分享 |
| `douyin_script.md` | 抖音 | 视频脚本 |

### Template Format

Each skill template uses Python string formatting:

```markdown
## 创作主题
{topic}

## 原始内容
{original_content}
```

You can customize these templates by editing the Markdown files directly.

## Usage Examples

### Example 1: Basic Usage

```python
from mcp_content_styles.skill_manager import SkillManager

manager = SkillManager()

# Get formatted prompt for 知乎
prompt = manager.format_skill(
    "zhihu_article",
    topic="AI工具测评",
    original_content="## 工具介绍\n\n这是一个AI工具..."
)

print(prompt)
```

### Example 2: Run Examples

```bash
cd /Users/kevinten/projects/mcp-content-styles
python examples/usage_example.py
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run specific test
pytest tests/test_skill_manager.py -v

# Check code style
flake8 src/
```

## Claude Desktop Integration

Add to your Claude Desktop config (`~/.config/claude/claude_desktop_config.json` on Linux/Mac or `%APPDATA%/Claude/claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "content-styles": {
      "command": "python",
      "args": ["-m", "mcp_content_styles.main"],
      "cwd": "/Users/kevinten/projects/mcp-content-styles"
    }
  }
}
```

Then restart Claude Desktop.

## License

MIT
