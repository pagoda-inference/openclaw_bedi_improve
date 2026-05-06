#!/usr/bin/env python3
"""
Unit tests for deep-browser-skill scripts
Run with: python tests/test_deep_browser_skill.py
"""

import sys
import os
import tempfile
import shutil
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / "deep-browser-skill" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from file_operations import FileOps
from memory_manager import MemoryManager
from init_environment import init_environment, check_opencli


class TestFileOps:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.md")

    def teardown_method(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_write_and_read(self):
        content = "# Test\n\nHello World"
        FileOps.write(self.test_file, content)
        result = FileOps.read(self.test_file)
        assert result == content
        print("✓ test_write_and_read passed")

    def test_read_nonexistent_file(self):
        result = FileOps.read("/nonexistent/path/file.md")
        assert result is None
        print("✓ test_read_nonexistent_file passed")

    def test_replace_lines(self):
        FileOps.write(self.test_file, "# Title\n\nLine 1\nLine 2\nLine 3\n")
        FileOps.replace_lines(self.test_file, 3, 4, ["New Line A", "New Line B"])
        result = FileOps.read(self.test_file)
        expected = "# Title\n\nNew Line A\nNew Line B\nLine 3\n"
        assert result == expected
        print("✓ test_replace_lines passed")

    def test_replace_section(self):
        content = "# Title\n\n## Section 1\nOld content\n## End Section\n\nFooter\n"
        FileOps.write(self.test_file, content)
        FileOps.replace_section(self.test_file, "## Section 1", "## End Section", "New content\n")
        result = FileOps.read(self.test_file)
        assert "New content" in result
        assert "Old content" not in result
        print("✓ test_replace_section passed")

    def test_append(self):
        FileOps.write(self.test_file, "# Title\n")
        FileOps.append(self.test_file, "Appended line")
        result = FileOps.read(self.test_file)
        assert "Appended line" in result
        print("✓ test_append passed")

    def test_insert_after(self):
        FileOps.write(self.test_file, "# Title\n\n## Section\n\nFooter")
        FileOps.insert_after(self.test_file, "## Section", ["New line 1", "New line 2"])
        result = FileOps.read(self.test_file)
        lines = result.split("\n")
        section_idx = next(i for i, l in enumerate(lines) if "## Section" in l)
        assert "New line 1" in lines[section_idx + 1]
        print("✓ test_insert_after passed")

    def test_delete_section(self):
        content = "# Title\n\n## Start\nContent to delete\n## End\n\nKeep this\n"
        FileOps.write(self.test_file, content)
        FileOps.delete_section(self.test_file, "## Start", "## End")
        result = FileOps.read(self.test_file)
        assert "Content to delete" not in result
        assert "Keep this" in result
        print("✓ test_delete_section passed")

    def test_create_nested_directory(self):
        nested_file = os.path.join(self.temp_dir, "a", "b", "c", "test.md")
        FileOps.write(nested_file, "Nested content")
        assert os.path.exists(nested_file)
        result = FileOps.read(nested_file)
        assert result == "Nested content"
        print("✓ test_create_nested_directory passed")


class TestMemoryManager:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_create_and_read_site_pattern(self):
        manager = MemoryManager()
        content = "# test-example.com\n\n> Domain: test-example.com\n\n## Page Types\n"
        path = manager.create_site_pattern("test-example.com", content)
        assert path.exists()
        result = manager.read_site_pattern("test-example.com")
        assert result == content
        print("✓ test_create_and_read_site_pattern passed")

    def test_read_nonexistent_pattern(self):
        manager = MemoryManager()
        result = manager.read_site_pattern("nonexistent-pattern.xyz")
        assert result is None
        print("✓ test_read_nonexistent_pattern passed")

    def test_list_patterns(self):
        manager = MemoryManager()
        manager.create_site_pattern("test-list-1.com", "# Test 1")
        manager.create_site_pattern("test-list-2.com", "# Test 2")
        patterns = manager.list_site_patterns()
        assert "test-list-1.com" in patterns
        assert "test-list-2.com" in patterns
        print("✓ test_list_patterns passed")

    def test_search_patterns(self):
        manager = MemoryManager()
        manager.create_site_pattern("test-search-1.com", "# Product listing\n\nProducts here")
        manager.create_site_pattern("test-search-2.com", "# About page\n\nAbout us")
        results = manager.search_patterns("product")
        assert "test-search-1.com" in results
        assert "test-search-2.com" not in results
        print("✓ test_search_patterns passed")

    def test_create_browsing_plan(self):
        manager = MemoryManager()
        content = "# Browsing Plan\n\n## Goal\nTest browsing\n"
        path = manager.create_browsing_plan("test-plan-001", content)
        assert path.exists()
        result = manager.read_browsing_plan("test-plan-001")
        assert result == content
        print("✓ test_create_browsing_plan passed")

    def test_index_creation(self):
        manager = MemoryManager()
        manager.create_site_pattern("test-index.com", "# Test")
        index_path = manager.sites_dir / "INDEX.md"
        assert index_path.exists()
        index_content = index_path.read_text()
        assert "test-index.com" in index_content
        print("✓ test_index_creation passed")


class TestInitEnvironment:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_init_creates_directories(self):
        result = init_environment()
        assert result == True
        skill_dir = SCRIPTS_DIR.parent
        assert (skill_dir / "browser-patterns" / "sites").exists()
        assert (skill_dir / "browser-patterns" / "plans").exists()
        assert (skill_dir / "states").exists()
        print("✓ test_init_creates_directories passed")

    def test_init_creates_index_files(self):
        init_environment()
        skill_dir = SCRIPTS_DIR.parent
        assert (skill_dir / "browser-patterns" / "sites" / "INDEX.md").exists()
        assert (skill_dir / "browser-patterns" / "plans" / "INDEX.md").exists()
        print("✓ test_init_creates_index_files passed")


class TestOpenCLICheck:
    def test_check_opencli(self):
        ok, msg = check_opencli()
        if ok:
            print(f"✓ OpenCLI available: {msg}")
        else:
            print(f"⊘ OpenCLI not available: {msg}")
            print("  (This is expected if OpenCLI is not installed)")


def run_all_tests():
    print("=" * 60)
    print("Running Deep Browser Skill Tests")
    print("=" * 60)
    print()

    print("--- Testing FileOps ---")
    file_ops_tests = TestFileOps()
    for method_name in dir(file_ops_tests):
        if method_name.startswith("test_"):
            file_ops_tests.setup_method()
            try:
                getattr(file_ops_tests, method_name)()
            except Exception as e:
                print(f"✗ {method_name} failed: {e}")
            finally:
                file_ops_tests.teardown_method()
    print()

    print("--- Testing MemoryManager ---")
    memory_tests = TestMemoryManager()
    for method_name in dir(memory_tests):
        if method_name.startswith("test_"):
            memory_tests.setup_method()
            try:
                getattr(memory_tests, method_name)()
            except Exception as e:
                print(f"✗ {method_name} failed: {e}")
            finally:
                memory_tests.teardown_method()
    print()

    print("--- Testing InitEnvironment ---")
    init_tests = TestInitEnvironment()
    for method_name in dir(init_tests):
        if method_name.startswith("test_"):
            init_tests.setup_method()
            try:
                getattr(init_tests, method_name)()
            except Exception as e:
                print(f"✗ {method_name} failed: {e}")
            finally:
                init_tests.teardown_method()
    print()

    print("--- Testing OpenCLI Check ---")
    opencli_tests = TestOpenCLICheck()
    try:
        opencli_tests.test_check_opencli()
    except Exception as e:
        print(f"✗ test_check_opencli failed: {e}")
    print()

    print("=" * 60)
    print("Tests completed")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
