#!/usr/bin/env python3
"""
Memory Manager
Simple pattern storage and retrieval with index mechanism
"""

from pathlib import Path
from datetime import datetime
from typing import List, Optional


class MemoryManager:
    """Simple pattern file manager with index"""
    
    def __init__(self):
        # Path(__file__) = memory_manager.py
        # .parent = scripts/
        # .parent.parent = deep-browser/ (skill根目录)
        skill_dir = Path(__file__).parent.parent
        self.base_dir = skill_dir / "browser-patterns"
        self.sites_dir = self.base_dir / "sites"
        self.plans_dir = self.base_dir / "plans"
        
        self.sites_dir.mkdir(parents=True, exist_ok=True)
        self.plans_dir.mkdir(parents=True, exist_ok=True)
    
    def create_site_pattern(self, domain: str, content: str) -> Path:
        """Create site pattern file"""
        file_path = self.sites_dir / f"{domain}.md"
        file_path.write_text(content, encoding="utf-8")
        self._update_index(self.sites_dir, domain)
        return file_path
    
    def read_site_pattern(self, domain: str) -> Optional[str]:
        """Read site pattern file"""
        file_path = self.sites_dir / f"{domain}.md"
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        return None
    
    def create_browsing_plan(self, plan_id: str, content: str) -> Path:
        """Create browsing plan file"""
        file_path = self.plans_dir / f"{plan_id}.md"
        file_path.write_text(content, encoding="utf-8")
        self._update_index(self.plans_dir, plan_id)
        return file_path
    
    def read_browsing_plan(self, plan_id: str) -> Optional[str]:
        """Read browsing plan file"""
        file_path = self.plans_dir / f"{plan_id}.md"
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        return None
    
    def list_site_patterns(self) -> List[str]:
        """List all site pattern IDs"""
        return [f.stem for f in self.sites_dir.glob("*.md") if f.stem != "INDEX"]
    
    def list_browsing_plans(self) -> List[str]:
        """List all browsing plan IDs"""
        return [f.stem for f in self.plans_dir.glob("*.md") if f.stem != "INDEX"]
    
    def search_patterns(self, query: str) -> List[str]:
        """Search patterns by content"""
        results = []
        query_lower = query.lower()
        
        for pattern_file in self.sites_dir.glob("*.md"):
            if pattern_file.stem == "INDEX":
                continue
            
            content = pattern_file.read_text(encoding="utf-8")
            if query_lower in content.lower():
                results.append(pattern_file.stem)
        
        return results
    
    def _update_index(self, directory: Path, entry_id: str):
        """Update index file"""
        index_path = directory / "INDEX.md"
        
        # Read existing index
        existing_entries = []
        if index_path.exists():
            content = index_path.read_text(encoding="utf-8")
            for line in content.split("\n"):
                if line.startswith("|") and entry_id in line:
                    return  # Already in index
        
        # Append new entry
        with open(index_path, "a", encoding="utf-8") as f:
            if not index_path.exists() or index_path.stat().st_size == 0:
                # Write header
                if directory == self.sites_dir:
                    f.write("# Website Patterns Index\n\n")
                    f.write("| Domain | File | Last Updated |\n")
                    f.write("|--------|------|-------------|\n")
                else:
                    f.write("# Browsing Plans Index\n\n")
                    f.write("| Plan ID | File | Last Updated |\n")
                    f.write("|---------|------|-------------|\n")
            
            # Write entry
            timestamp = datetime.now().strftime("%Y-%m-%d")
            f.write(f"| {entry_id} | [{entry_id}.md](./{entry_id}.md) | {timestamp} |\n")


if __name__ == "__main__":
    manager = MemoryManager()
    
    # Test create pattern
    pattern_content = """# example.com

> Domain: example.com
> Created: 2026-04-28

## Page Types

### listing

- Product grid layout
- Pagination controls

## Selectors

- search_box: #search
- submit_btn: .search-btn
"""
    
    path = manager.create_site_pattern("example.com", pattern_content)
    print(f"Created: {path}")
    
    # Test read
    content = manager.read_site_pattern("example.com")
    print(f"Content length: {len(content) if content else 0}")
    
    # Test search
    results = manager.search_patterns("product")
    print(f"Search results: {results}")
    
    # Test list
    patterns = manager.list_site_patterns()
    print(f"All patterns: {patterns}")
