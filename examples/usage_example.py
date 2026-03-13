#!/usr/bin/env python3
"""
Usage example for mcp-content-styles MCP server.

This script demonstrates how to use the content styles MCP server
to convert markdown content for different platforms.
"""

import json
from mcp_content_styles.skill_manager import SkillManager


def example_1_basic_skill_usage():
    """Example 1: Basic skill loading and formatting."""
    print("=" * 60)
    print("Example 1: Basic Skill Usage")
    print("=" * 60)

    # Initialize skill manager
    manager = SkillManager()

    # List available skills
    print("\nAvailable Skills:")
    for skill in manager.list_skills():
        print(f"  - {skill['name']}: {skill['description']}")

    # Get a specific skill
    print("\n--- Zhihu Article Skill ---")
    content = manager.get_skill("zhihu_article")
    print(content[:500] + "...")


def example_2_format_skill_with_params():
    """Example 2: Format skill with custom parameters."""
    print("\n" + "=" * 60)
    print("Example 2: Format Skill with Parameters")
    print("=" * 60)

    manager = SkillManager()

    # Original markdown content
    original_content = """
# AI Tools for Content Creation

I've been experimenting with various AI tools for content creation.
Here are my findings:

## Key Benefits

1. **Efficiency**: AI can help write faster
2. **Quality**: Consistent output quality
3. **Scale**: Produce more content

## Conclusion

AI tools are transforming how we create content.
"""

    # Format for Zhihu
    formatted = manager.format_skill(
        "zhihu_article",
        topic="AI内容创作工具探索",
        original_content=original_content
    )

    print("\n--- Formatted Prompt for Zhihu ---")
    print(formatted[:800] + "...")


def example_3_platform_conversion():
    """Example 3: Convert content for different platforms."""
    print("\n" + "=" * 60)
    print("Example 3: Platform Conversion")
    print("=" * 60)

    manager = SkillManager()

    original_content = """
今天想和大家分享一个非常实用的AI工具 - Claude Code。
它可以帮助开发者更高效地编写代码，提供智能代码补全和错误检测功能。
"""

    platforms = [
        ("xiaohongshu_note", "小红书"),
        ("weibo_post", "微博"),
        ("douyin_script", "抖音"),
    ]

    for skill_name, platform_name in platforms:
        print(f"\n--- {platform_name} Format ---")
        formatted = manager.format_skill(
            skill_name,
            topic="Claude Code AI工具分享",
            original_content=original_content
        )
        # Print first 400 chars
        print(formatted[:400] + "...")


def example_4_workflow_simulation():
    """Example 4: Complete workflow simulation."""
    print("\n" + "=" * 60)
    print("Example 4: Complete Workflow")
    print("=" * 60)

    manager = SkillManager()

    # Step 1: User writes original content
    user_content = """
# MCP (Model Context Protocol) 介绍

MCP 是一种开放协议，用于标准化 AI 模型与外部工具的集成。

## 核心优势

- **标准化**: 统一的接口规范
- **互操作性**: 不同厂商的 AI 都能使用
- **可扩展性**: 轻松添加新功能

## 应用场景

MCP 适用于各种 AI 增强型应用，从代码编辑器到数据分析工具。
"""

    print("\n[Step 1] Original content written")
    print(f"Content length: {len(user_content)} chars")

    # Step 2: Choose platform and mode
    platform = "wechat_article"
    mode = "format"

    print(f"\n[Step 2] Selected platform: {platform}, mode: {mode}")

    # Step 3: Get formatted prompt
    prompt = manager.format_skill(
        platform,
        topic="MCP协议深度解析",
        original_content=user_content
    )

    print(f"\n[Step 3] Generated prompt ({len(prompt)} chars)")
    print("\nPrompt preview:")
    print("-" * 40)
    print(prompt[:600])
    print("-" * 40)

    # Step 4: Instructions for next steps
    print("\n[Step 4] Next steps:")
    print("  1. Send this prompt to LLM")
    print("  2. Use LLM output to generate images (mcp-image)")
    print("  3. Use LLM output to generate videos (mcp-video-gen)")
    print("  4. Publish to platform via platform-specific MCP")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("MCP Content Styles - Usage Examples")
    print("=" * 60)

    example_1_basic_skill_usage()
    example_2_format_skill_with_params()
    example_3_platform_conversion()
    example_4_workflow_simulation()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
