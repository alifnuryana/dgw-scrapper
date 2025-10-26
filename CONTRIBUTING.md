# Contributing to DGW Scrapper

First off, thank you for considering contributing to DGW Scrapper! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to maintaining a welcoming and respectful environment. Please be kind and courteous to others.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear descriptive title**
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear descriptive title**
- **Detailed description** of the proposed functionality
- **Why this enhancement would be useful**
- **Possible implementation** (if you have ideas)

### Pull Requests

1. Fork the repo and create your branch from `main`
2. Make your changes
3. Test your changes thoroughly
4. Update documentation if needed
5. Submit a pull request

## Development Setup

1. **Clone your fork**

```bash
git clone https://github.com/YOUR_USERNAME/dgw-scrapper.git
cd dgw-scrapper
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
playwright install chromium
```

4. **Create a branch for your feature**

```bash
git checkout -b feature/your-feature-name
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Maximum line length: 100 characters

### Example Function Documentation

```python
def process_data(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Process dataframe by cleaning and transforming data.

    Args:
        df (pd.DataFrame): Input dataframe to process
        column (str): Name of the column to transform

    Returns:
        pd.DataFrame: Processed dataframe

    Raises:
        ValueError: If column doesn't exist in dataframe
    """
    # Implementation here
    pass
```

### Code Organization

- Keep related functionality together
- Use helper functions for repeated logic
- Add comments for complex operations
- Handle errors gracefully

## Commit Messages

### Format

```
<type>: <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat: add support for multiple document types

Added command-line option to specify document type filter
beyond just LPJ documents.

Closes #123
```

```
fix: handle timeout errors gracefully

The scraper now continues processing remaining items
when a timeout occurs instead of crashing.
```

## Pull Request Process

1. **Update documentation** to reflect any changes
2. **Add tests** if applicable
3. **Ensure all tests pass**
4. **Update the README.md** with details of changes if needed
5. **Reference any related issues** in your PR description

### PR Checklist

- [ ] Code follows the project's style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Changes tested locally

### Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

---

Thank you for contributing! 🙌
