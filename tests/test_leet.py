import json
import os
import sys
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from leet import load_config, main
from cli.utils.config_manager import ConfigManager


class TestLoadConfig:
    
    def test_load_config_returns_dict(self):
        config = load_config()
        assert isinstance(config, dict)
    
    def test_load_config_has_required_keys(self):
        config = load_config()
        assert "base_dir" in config
        assert "data_structures" in config
    
    def test_load_config_data_structures_valid(self):
        config = load_config()
        assert isinstance(config["data_structures"], dict)
        assert len(config["data_structures"]) > 0
        
        for key, value in config["data_structures"].items():
            assert isinstance(key, str)
            assert isinstance(value, str)


class TestMainFunction:
    
    def test_main_no_args_prints_usage(self, capsys):
        with patch.object(sys, 'argv', ['leet']):
            main()
            captured = capsys.readouterr()
            assert "Usage: leet" in captured.out or "Usage: leet" in captured.err
    
    def test_main_invalid_command_prints_error(self, capsys):
        with patch.object(sys, 'argv', ['leet', 'invalid-command']):
            main()
            captured = capsys.readouterr()
            assert "Unknown command" in captured.out or "Unknown command" in captured.err
    
    def test_main_recognizes_add_command(self):
        with patch.object(sys, 'argv', ['leet', 'add']):
            with patch('cli.commands.add_problem.main') as mock_add_main:
                main()
                mock_add_main.assert_called_once()
    
    def test_main_recognizes_add_sol_command(self):
        with patch.object(sys, 'argv', ['leet', 'add-sol']):
            with patch('cli.commands.add_solution.main') as mock_add_sol_main:
                main()
                mock_add_sol_main.assert_called_once()


class TestConfigValid:
    
    def test_config_json_exists(self):
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config.json"
        )
        assert os.path.exists(config_path), "config.json not found"
    
    def test_config_json_is_valid_json(self):
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config.json"
        )
        with open(config_path, 'r') as f:
            try:
                json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"config.json is not valid JSON: {e}")
    
    def test_config_json_base_dir_is_string(self):
        config = load_config()
        assert isinstance(config["base_dir"], str)
        assert len(config["base_dir"]) > 0


class TestCodeQuality:
    
    def test_leet_module_imports_successfully(self):
        try:
            import leet
            assert hasattr(leet, 'main')
            assert hasattr(leet, 'load_config')
        except ImportError as e:
            pytest.fail(f"Failed to import leet module: {e}")
    
    def test_add_problem_module_imports_successfully(self):
        try:
            from cli.commands import add_problem
            assert hasattr(add_problem, 'main')
        except ImportError as e:
            pytest.fail(f"Failed to import add_problem module: {e}")
    
    def test_add_solution_module_imports_successfully(self):
        try:
            from cli.commands import add_solution
            assert hasattr(add_solution, 'main')
        except ImportError as e:
            pytest.fail(f"Failed to import add_solution module: {e}")
    
    def test_config_manager_imports_successfully(self):
        try:
            from cli.utils.config_manager import ConfigManager
            config_manager = ConfigManager()
            assert hasattr(config_manager, 'get_data_structures')
            assert hasattr(config_manager, 'add_data_structure')
        except ImportError as e:
            pytest.fail(f"Failed to import ConfigManager: {e}")


class TestAddFunctionality:
    
    def test_file_utils_count_solutions_empty_content(self):
        from cli.utils.file_utils import count_solutions
        result = count_solutions("")
        assert result == 0
    
    def test_file_utils_count_solutions_single(self):
        from cli.utils.file_utils import count_solutions
        content = "Solution 1\nCode here"
        result = count_solutions(content)
        assert result == 1
    
    def test_file_utils_count_solutions_multiple(self):
        from cli.utils.file_utils import count_solutions
        content = "Solution 1\nCode\nSolution 2\nMore code"
        result = count_solutions(content)
        assert result == 2
    
    def test_config_manager_get_data_structures(self):
        config_manager = ConfigManager()
        structures = config_manager.get_data_structures()
        assert isinstance(structures, dict)
        assert len(structures) > 0
