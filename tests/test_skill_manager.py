"""Tests for the skill manager module."""

import os
import pytest
from mcp_content_styles.skill_manager import SkillManager


class TestSkillManager:
    """Test cases for SkillManager class."""

    def test_init_default_directory(self):
        """Test initialization with default directory."""
        manager = SkillManager()
        assert manager.skills_dir is not None
        assert os.path.exists(manager.skills_dir)

    def test_init_custom_directory(self):
        """Test initialization with custom directory."""
        custom_dir = "/tmp/test_skills"
        manager = SkillManager(custom_dir)
        assert manager.skills_dir == custom_dir

    def test_load_skills(self):
        """Test loading skills from directory."""
        manager = SkillManager()
        assert len(manager.skills) > 0

    def test_get_skill_exists(self):
        """Test getting an existing skill."""
        manager = SkillManager()
        # Should have at least one of the platform skills
        content = manager.get_skill("zhihu_article")
        assert content is not None
        assert "知乎" in content or "zhihu" in content.lower()

    def test_get_skill_not_exists(self):
        """Test getting a non-existent skill."""
        manager = SkillManager()
        content = manager.get_skill("non_existent_skill")
        assert content is None

    def test_format_skill_with_params(self):
        """Test formatting a skill with parameters."""
        manager = SkillManager()
        result = manager.format_skill(
            "zhihu_article",
            topic="Test Topic",
            original_content="Test content"
        )
        assert result is not None
        assert "Test Topic" in result
        assert "Test content" in result

    def test_format_skill_not_exists(self):
        """Test formatting a non-existent skill."""
        manager = SkillManager()
        result = manager.format_skill("non_existent", topic="Test")
        assert result is None

    def test_list_skills(self):
        """Test listing all available skills."""
        manager = SkillManager()
        skills = manager.list_skills()
        assert len(skills) > 0

        # Check structure of returned skills
        for skill in skills:
            assert "name" in skill
            assert "description" in skill
            assert "file" in skill

    def test_has_skill(self):
        """Test checking if skill exists."""
        manager = SkillManager()
        assert manager.has_skill("zhihu_article") is True
        assert manager.has_skill("non_existent") is False

    def test_format_skill_with_missing_param(self):
        """Test formatting with missing optional parameters."""
        manager = SkillManager()
        # Should not raise exception even with missing params
        result = manager.format_skill("zhihu_article", topic="Only Topic")
        assert result is not None
