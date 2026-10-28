# Contributing to Cyberkill.ai

Thank you for your interest in contributing to **Cyberkill.ai**!

## Development Setup
1. Fork and clone the repository:
   ```bash
   git clone https://github.com/<your-username>/cyberkill-ai.git
   cd cyberkill-ai
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```
4. Run tests:
   ```bash
   PYTHONPATH=src python3 -m unittest discover tests
   ```

## Guidelines
- Strict Scope Guard: Any tool addition must respect ethical boundaries and ScopeGuard.
- Typing: Use Type Hints across all modules.
- Pull Requests: Target the `main` branch with descriptive commit messages.
