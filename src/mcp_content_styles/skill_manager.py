"""
Skill Manager - Manages platform-specific prompt templates
"""

from pathlib import Path
from typing import List, Dict, Optional
from loguru import logger


class SkillManager:
    """Manages loading and formatting of skill templates"""

    def __init__(self, skills_dir: Optional[str] = None):
        """
        Initialize skill manager

        Args:
            skills_dir: Path to skills directory. If None, uses default.
        """
        if skills_dir is None:
            current_file = Path(__file__).resolve()
            skills_dir = current_file.parent / "skills"

        self.skills_dir = Path(skills_dir)
        self.skills: List[Dict[str, str]] = []
        self._load_all_skills()

    def _load_all_skills(self):
        """Load all skills from markdown files"""
        if not self.skills_dir.exists():
            logger.warning(f"Skills directory not found: {self.skills_dir}")
            return

        for skill_file in self.skills_dir.glob("*.md"):
            skill = self._parse_skill_file(skill_file)
            if skill:
                self.skills.append(skill)

        logger.info(f"Loaded {len(self.skills)} skills from {self.skills_dir}")

    def _parse_skill_file(self, file_path: Path) -> Optional[Dict[str, str]]:
        """
        Parse a skill markdown file

        Format:
        # Skill Name
        > Description

        Content with {placeholders}...
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.strip().split('\n')

            name = file_path.stem
            description = ""
            skill_content = []
            header_found = False
            description_found = False

            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith('# ') and not header_found:
                    name = line[2:].strip()
                    header_found = True
                elif line.startswith('> ') and not description_found:
                    description = line[2:].strip()
                    description_found = True
                elif line:
                    skill_content.append(lines[i])
                i += 1

            return {
                "name": name,
                "description": description or f"{name} skill template",
                "content": '\n'.join(skill_content),
                "file_stem": file_path.stem
            }
        except Exception as e:
            logger.error(f"Failed to parse skill file {file_path}: {e}")
            return None

    def get_skill(self, skill_name: str) -> Optional[str]:
        """Get skill content by name"""
        for skill in self.skills:
            if skill["name"] == skill_name:
                return skill["content"]

        for skill in self.skills:
            if skill.get("file_stem") == skill_name:
                return skill["content"]

        return None

    def format_skill(self, skill_name: str, **kwargs) -> Optional[str]:
        """
        Format skill content with parameter substitution

        Args:
            skill_name: Name of the skill
            **kwargs: Parameters for substitution

        Returns:
            Formatted content or None if skill not found
        """
        content = self.get_skill(skill_name)
        if content is None:
            return None

        if kwargs:
            try:
                return content.format(**kwargs)
            except KeyError as e:
                logger.warning(f"Missing parameter for skill '{skill_name}': {e}")
                return content
            except Exception as e:
                logger.error(f"Error formatting skill '{skill_name}': {e}")
                return content

        return content

    def list_skills(self) -> List[Dict[str, str]]:
        """List all available skills (name and description only)"""
        return [{"name": s["name"], "description": s["description"]} for s in self.skills]

    def has_skill(self, skill_name: str) -> bool:
        """Check if skill exists"""
        return self.get_skill(skill_name) is not None
