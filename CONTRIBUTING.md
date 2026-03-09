# Contributing to BingX Python SDK

Thank you for considering contributing to the BingX Python SDK! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/bingx-python.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests and linting
6. Commit your changes
7. Push to your fork
8. Create a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/tigusigalpa/bingx-python.git
cd bingx-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
pip install -e .
```

## Code Style

This project follows PEP 8 style guidelines with some modifications:

- Line length: 100 characters
- Use type hints where possible
- Use docstrings for all public methods and classes
- Format code with Black: `black bingx/`
- Check with flake8: `flake8 bingx/`

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=bingx --cov-report=html

# Run specific test file
pytest tests/test_client.py
```

## Type Checking

```bash
# Run mypy type checker
mypy bingx --ignore-missing-imports
```

## Commit Messages

- Use clear and descriptive commit messages
- Start with a verb in present tense (Add, Fix, Update, Remove, etc.)
- Reference issue numbers when applicable

Examples:
- `Add support for TWAP orders`
- `Fix authentication error handling`
- `Update market service documentation`

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add tests for new features
4. Update CHANGELOG.md with your changes
5. Ensure your code follows the style guidelines
6. Create a Pull Request with a clear description

## Reporting Bugs

When reporting bugs, please include:

- Python version
- BingX Python SDK version
- Minimal code to reproduce the issue
- Expected behavior
- Actual behavior
- Error messages and stack traces

## Feature Requests

Feature requests are welcome! Please:

- Check if the feature already exists
- Provide a clear use case
- Explain why this feature would be useful
- Consider submitting a Pull Request

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
