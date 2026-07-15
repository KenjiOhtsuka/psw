# Contributing to PSW

Thank you for your interest in contributing to PSW! This document provides guidelines for setting up your development environment, running tests, and submitting your contributions.

---

## 🛠️ Development Environment Setup

To run and test the program during development without installing it globally, you need to add the `src` directory to your `PYTHONPATH` environment variable. 

Choose the command corresponding to your operating system and terminal:

### macOS / Linux (Bash, Zsh, etc.)

```bash
export PYTHONPATH=src
python -m psw timer 5s
```

### Windows (PowerShell)

```powershell
$env:PYTHONPATH="src"
python -m psw timer 5s
```

### Windows (Command Prompt - `cmd.exe`)

```cmd
set PYTHONPATH=src
python -m psw timer 5s
```

## 🧪 Testing

We use `pytest` for running our automated test suite. Before running tests, ensure you have the development dependencies installed.

### 1. Install Development Dependencies

Navigate to the root directory of the project and install the package in editable mode with test dependencies:

```bash
pip install -e ".[test]"
```

### 2. Run Tests

You can run the tests using either of the following commands:

```bash
# Recommended
python -m pytest tests

# Alternative
pytest
```

## 🤝 How to Contribute

### 1. Reporting Bugs & Suggesting Features

* Check the [Issues] tab to see if your bug or feature request has already been reported.
* If not, open a new issue. Please provide a clear description, steps to reproduce (for bugs), and your OS/Python version.

### 2. Submitting Pull Requests

1. **Fork** the repository and create your branch from `main`.
    ```bash
    git checkout -b feature/your-feature-name
    ```
2. **Implement your changes** and make sure you adhere to the project's coding style.
3. **Write tests** for any new functionality or bug fixes.
4. **Run the test suite** to ensure everything passes:
    ```bash
    python -m pytest tests
    ```
5. **Commit your changes** with a clear and descriptive commit message.
6. **Push** to your fork and **submit a Pull Request (PR)** to the `main` branch of this repository.

## 🎨 Coding Guidelines

To keep the codebase clean and consistent, please follow these guidelines:

* **PEP 8**: Follow standard Python coding style guidelines.
* **Type Hints**: Use type hinting for function arguments and return values where appropriate.
* **Docstrings**: Add docstrings to new classes and functions to explain their purpose and behavior.

## To Build Package

```
# 1. Install packaging tool
pip install pyinstaller

# 2. Build
python -m PyInstaller --onefile --paths src --name psw src/psw/__main__.py
```