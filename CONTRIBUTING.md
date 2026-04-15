# Contributing to LeetCode CLI

Thank you for considering to contribute to this project! Here are some guidelines to help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/leetcode-cli.git`
3. Create a new branch: `git checkout -b feat/your-feature-name`
4. Install dependencies: `pip install -r requirements-dev.txt`

## Before You Commit

### Run Tests Locally
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=.

# Run linting
flake8 .
```

### Make Sure Tests Pass
All tests must pass before submitting a pull request:
```bash
pytest tests/
```

If any tests fail, please fix them before pushing.

## Workflow

1. **Create a feature branch**: `git checkout -b feat/my-feature`
2. **Make your changes** and test locally
3. **Commit your changes** with clear commit messages
4. **Push to your fork**: `git push origin feat/my-feature`
5. **Open a Pull Request** with a clear description

## Pull Request Requirements

Before your PR can be merged:

✅ **All tests must pass** - GitHub Actions will automatically run tests  
✅ **Code must be linted** - flake8 checks must pass  
✅ **At least one reviewer approval** (if configured)  
✅ **Branch must be up to date** with main

## Automated Checks

GitHub Actions will automatically check your PR:

- **tests.yml**: Runs pytest on Python 3.8, 3.9, 3.10, 3.11
- **python-lint.yml**: Checks code quality with flake8 and pylint

If any check fails, you'll see a red ❌ indicator. Fix the issues and push again.

## Adding Tests

When adding new features, please include tests:

1. Create test cases in `tests/test_leet.py`
2. Use descriptive names: `test_<function>_<scenario>`
3. Add docstrings to explain what's being tested
4. Run `pytest` to verify tests pass

Example:
```python
def test_my_new_feature_works_correctly(self):
    """Test that my new feature handles all cases correctly"""
    result = my_function()
    assert result == expected_value
```

## Code Style

- Follow PEP 8 guidelines
- Use descriptive variable and function names
- Add comments for complex logic
- Keep functions focused and small

## Questions?

Feel free to open an issue with questions or suggestions!
