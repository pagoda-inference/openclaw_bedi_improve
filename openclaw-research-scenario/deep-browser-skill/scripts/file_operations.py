#!/usr/bin/env python3
"""
File Operations
Simple file manipulation utilities for state management
"""

from pathlib import Path
from typing import List, Optional


class FileOps:
    """Simple file operations for state and pattern files"""
    
    @staticmethod
    def read(file_path: str) -> Optional[str]:
        """Read file content"""
        path = Path(file_path)
        if path.exists():
            return path.read_text(encoding="utf-8")
        return None
    
    @staticmethod
    def write(file_path: str, content: str):
        """Write content to file"""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    
    @staticmethod
    def replace_section(
        file_path: str,
        start_marker: str,
        end_marker: str,
        new_content: str
    ):
        """Replace a section between markers"""
        content = FileOps.read(file_path)
        if not content:
            return
        
        lines = content.split("\n")
        new_lines = []
        in_section = False
        
        for line in lines:
            if start_marker in line:
                in_section = True
                new_lines.append(line)
                new_lines.append(new_content)
            elif end_marker in line and in_section:
                in_section = False
                new_lines.append(line)
            elif not in_section:
                new_lines.append(line)
        
        FileOps.write(file_path, "\n".join(new_lines))
    
    @staticmethod
    def replace_lines(
        file_path: str,
        start_line: int,
        end_line: int,
        new_lines: List[str]
    ):
        """Replace lines by line numbers (1-indexed)"""
        content = FileOps.read(file_path)
        if not content:
            return
        
        lines = content.split("\n")
        
        # Adjust to 0-indexed
        start_idx = max(0, start_line - 1)
        end_idx = min(len(lines), end_line)
        
        # Replace lines
        new_content = lines[:start_idx] + new_lines + lines[end_idx:]
        
        FileOps.write(file_path, "\n".join(new_content))
    
    @staticmethod
    def insert_after(
        file_path: str,
        marker: str,
        new_lines: List[str]
    ):
        """Insert lines after a marker"""
        content = FileOps.read(file_path)
        if not content:
            return
        
        lines = content.split("\n")
        new_content = []
        
        for line in lines:
            new_content.append(line)
            if marker in line:
                new_content.extend(new_lines)
        
        FileOps.write(file_path, "\n".join(new_content))
    
    @staticmethod
    def delete_section(
        file_path: str,
        start_marker: str,
        end_marker: str
    ):
        """Delete a section between markers"""
        content = FileOps.read(file_path)
        if not content:
            return
        
        lines = content.split("\n")
        new_lines = []
        in_section = False
        
        for line in lines:
            if start_marker in line:
                in_section = True
            elif end_marker in line and in_section:
                in_section = False
                continue
            
            if not in_section:
                new_lines.append(line)
        
        FileOps.write(file_path, "\n".join(new_lines))
    
    @staticmethod
    def append(file_path: str, content_to_add: str):
        """Append content to file"""
        content = FileOps.read(file_path)
        if content:
            new_content = content + "\n" + content_to_add
        else:
            new_content = content_to_add
        
        FileOps.write(file_path, new_content)


if __name__ == "__main__":
    # Test file operations
    test_file = "/tmp/test_file_ops.md"
    
    # Write
    FileOps.write(test_file, "# Test\n\nLine 1\nLine 2\nLine 3\n")
    print(f"Written to {test_file}")
    
    # Read
    content = FileOps.read(test_file)
    print(f"Content:\n{content}")
    
    # Replace lines
    FileOps.replace_lines(test_file, 3, 4, ["New Line 1", "New Line 2"])
    print(f"After replace:\n{FileOps.read(test_file)}")
    
    # Append
    FileOps.append(test_file, "Appended line")
    print(f"After append:\n{FileOps.read(test_file)}")
