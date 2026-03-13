"""Tests for the MCP server tools."""

import pytest
from mcp_content_styles.main import (
    get_platform_prompt,
    list_platforms,
    convert_content,
    get_skill_content,
)


class TestGetPlatformPrompt:
    """Test cases for get_platform_prompt tool."""

    def test_zhihu_article_format(self):
        """Test getting prompt for Zhihu article in format mode."""
        result = get_platform_prompt(
            platform="zhihu",
            content_type="article",
            mode="format",
            topic="AI Tools",
            original_content="Test content"
        )
        assert "知乎" in result or "技术" in result
        assert "AI Tools" in result
        assert "Test content" in result

    def test_wechat_article_rewrite(self):
        """Test getting prompt for WeChat article in rewrite mode."""
        result = get_platform_prompt(
            platform="wechat",
            content_type="article",
            mode="rewrite",
            topic="Python Tips",
            original_content="Some tips"
        )
        assert result is not None
        assert "Python Tips" in result

    def test_xiaohongshu_note(self):
        """Test getting prompt for Xiaohongshu note."""
        result = get_platform_prompt(
            platform="xiaohongshu",
            content_type="note",
            mode="format",
            topic="Productivity",
            original_content="Test"
        )
        assert result is not None
        assert "Productivity" in result

    def test_weibo_post(self):
        """Test getting prompt for Weibo post."""
        result = get_platform_prompt(
            platform="weibo",
            content_type="post",
            mode="format",
            topic="Tech News",
            original_content="Test"
        )
        assert result is not None

    def test_douyin_script(self):
        """Test getting prompt for Douyin script."""
        result = get_platform_prompt(
            platform="douyin",
            content_type="script",
            mode="rewrite",
            topic="AI Tutorial",
            original_content="Test"
        )
        assert result is not None

    def test_invalid_platform(self):
        """Test error handling for invalid platform."""
        result = get_platform_prompt(
            platform="invalid_platform",
            content_type="article",
            mode="format",
            topic="Test",
            original_content="Test"
        )
        assert "Error" in result or "not found" in result.lower()


class TestListPlatforms:
    """Test cases for list_platforms tool."""

    def test_returns_formatted_list(self):
        """Test that platform list is formatted."""
        result = list_platforms()
        assert "知乎" in result
        assert "公众号" in result
        assert "小红书" in result

    def test_contains_all_platforms(self):
        """Test that all supported platforms are listed."""
        result = list_platforms()
        platforms = ["知乎", "公众号", "小红书", "微博", "抖音"]
        for platform in platforms:
            assert platform in result


class TestConvertContent:
    """Test cases for convert_content tool."""

    def test_convert_with_markdown(self):
        """Test converting markdown content."""
        markdown = "# Test\n\nThis is a test article."
        result = convert_content(
            markdown_content=markdown,
            platform="zhihu",
            mode="format"
        )
        assert "Test" in result
        assert "转换指令" in result or "知乎" in result

    def test_empty_content(self):
        """Test handling of empty content."""
        result = convert_content(
            markdown_content="",
            platform="xiaohongshu",
            mode="format"
        )
        # Should still return instructions
        assert result is not None


class TestGetSkillContent:
    """Test cases for get_skill_content tool."""

    def test_get_existing_skill(self):
        """Test getting content of an existing skill."""
        result = get_skill_content("zhihu_article")
        assert result is not None
        assert len(result) > 0

    def test_get_nonexistent_skill(self):
        """Test getting content of a non-existent skill."""
        result = get_skill_content("nonexistent_skill_xyz")
        assert "Error" in result or "not found" in result.lower()
