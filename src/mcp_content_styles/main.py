"""
MCP Content Styles Server
Provides platform-specific content creation prompts
"""

from mcp.server.fastmcp import FastMCP
from .skill_manager import SkillManager
from loguru import logger

# Configure logging
logger.add("mcp_content_styles.log", rotation="10 MB")

# Create MCP server
mcp = FastMCP("content-styles")

# Initialize skill manager
skill_manager = SkillManager()


@mcp.tool()
def get_platform_prompt(
    platform: str,
    content_type: str,
    mode: str = "format",
    topic: str = "",
    original_content: str = ""
) -> str:
    """
    Get platform-specific content creation prompt

    Args:
        platform: Platform name (zhihu, wechat, xiaohongshu, weibo, douyin, x, juejin, csdn, devto, medium, bluesky, hackernews)
        content_type: Content type (article, note, post, script, image)
        mode: Processing mode - "format" (keep structure) or "rewrite" (rewrite style)
        topic: Topic for rewrite mode
        original_content: Original markdown content

    Returns:
        Complete prompt template for the platform
    """
    try:
        # Build skill name
        skill_name = f"{platform}_{content_type}"

        # Check if skill exists
        if not skill_manager.has_skill(skill_name):
            available = skill_manager.list_skills()
            available_names = [s["name"] for s in available]
            return (
                f"❌ Skill not found: '{skill_name}'\n\n"
                f"Available skills: {', '.join(available_names) or 'None'}"
            )

        # Format skill with parameters
        prompt = skill_manager.format_skill(
            skill_name,
            platform=platform,
            content_type=content_type,
            mode=mode,
            topic=topic,
            original_content=original_content
        )

        if prompt is None:
            return f"❌ Failed to load skill: {skill_name}"

        logger.info(f"✅ Returned prompt for {platform}/{content_type} (mode: {mode})")
        return prompt

    except Exception as e:
        logger.error(f"❌ Error in get_platform_prompt: {e}")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def list_platforms() -> str:
    """
    List all available platforms and content types

    Returns:
        Formatted list of available platforms
    """
    try:
        skills = skill_manager.list_skills()

        if not skills:
            return "❌ No skills available. Check skills directory."

        # Group by platform
        platforms = {}
        for skill in skills:
            parts = skill["name"].split("_")
            if len(parts) >= 2:
                platform = parts[0]
                content_type = "_".join(parts[1:])

                if platform not in platforms:
                    platforms[platform] = []
                platforms[platform].append(content_type)

        # Format output
        emojis = {
            "zhihu": "📝",
            "wechat": "📰",
            "xiaohongshu": "📕",
            "weibo": "📢",
            "douyin": "🎬",
            "x": "🐦",
            "juejin": "💎",
            "csdn": "📘",
            "devto": "👩‍💻",
            "medium": "📓",
            "bluesky": "🦋",
            "hackernews": "🟠"
        }

        result = "# 📱 Available Platforms\n\n"
        for platform, types in sorted(platforms.items()):
            emoji = emojis.get(platform, "📄")
            result += f"{emoji} **{platform}**: {', '.join(sorted(types))}\n"

        result += f"\n_Total: {len(skills)} skills_"

        return result

    except Exception as e:
        logger.error(f"❌ Error in list_platforms: {e}")
        return f"❌ Error: {str(e)}"


@mcp.tool()
def convert_content(
    markdown_content: str,
    platform: str,
    mode: str = "format"
) -> str:
    """
    Convert markdown content to platform-specific format

    Args:
        markdown_content: Original markdown content
        platform: Target platform
        mode: Processing mode (format or rewrite)

    Returns:
        Conversion instructions + prompt
    """
    # Detect content type from markdown
    content_type = "article"  # Default

    if platform == "xiaohongshu":
        content_type = "note"
    elif platform in ("weibo", "x", "bluesky", "hackernews"):
        content_type = "post"
    elif platform == "douyin":
        content_type = "script"

    # Get the prompt
    prompt = get_platform_prompt(
        platform=platform,
        content_type=content_type,
        mode=mode,
        original_content=markdown_content
    )

    if prompt.startswith("❌"):
        return prompt

    # Add usage instructions
    result = f"""# Content Conversion for {platform}

## Original Content
```markdown
{markdown_content[:500]}{"..." if len(markdown_content) > 500 else ""}
```

## Instructions
Use the following prompt with your LLM to convert the content:

---

{prompt}

---

## Next Steps
1. Copy the prompt above
2. Use with your preferred LLM (Claude, GPT, etc.)
3. Review and refine the output
4. Use mcp-image or mcp-video-gen to create media
5. Publish to {platform}
"""

    return result


@mcp.tool()
def get_skill_content(skill_name: str) -> str:
    """
    Get raw skill template content

    Args:
        skill_name: Name of the skill (e.g., "zhihu_article")

    Returns:
        Raw skill template markdown
    """
    content = skill_manager.get_skill(skill_name)

    if content is None:
        available = skill_manager.list_skills()
        available_names = [s["name"] for s in available]
        return (
            f"❌ Skill not found: '{skill_name}'\n\n"
            f"Available: {', '.join(available_names) or 'None'}"
        )

    return content


if __name__ == "__main__":
    mcp.run()
