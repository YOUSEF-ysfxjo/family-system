# Contributing to Family System

Thank you for your interest in contributing! The following guidelines will help you get started.

## Code of Conduct

By participating in this project you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

1. Search [existing issues](https://github.com/YOUSEF-ysfxjo/family-system/issues) to avoid duplicates.
2. Open a new issue using the **Bug Report** template.
3. Include clear reproduction steps, your environment details, and any relevant screenshots or logs.

### Suggesting Features

1. Search [existing issues](https://github.com/YOUSEF-ysfxjo/family-system/issues) to avoid duplicates.
2. Open a new issue using the **Feature Request** template.
3. Explain the problem you are solving and why this feature would benefit the project.

### Submitting a Pull Request

1. **Fork** the repository and create your branch from `main`:

   ```bash
   git checkout -b feature/my-feature
   ```

2. **Set up the development environment** (see [README.md](README.md)).

3. **Make your changes** and ensure they follow the coding style described below.

4. **Test your changes** locally before opening a pull request.

5. **Commit** using clear, conventional commit messages:

   ```
   feat: add similarity threshold slider
   fix: correct embedding normalization
   docs: update setup instructions
   ```

6. **Push** your branch and open a pull request against `main`. Fill in the PR template completely.

7. **Address review feedback** promptly; a maintainer will merge once everything looks good.

## Coding Style

- **Python**: Follow [PEP 8](https://pep8.org/). Keep lines under 100 characters.
- **JavaScript / React**: Follow the existing code style (ESLint configuration if present).
- **Commit messages**: Use [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `chore:`, etc.).

## Development Setup

See [README.md](README.md) for full setup instructions.

### Quick start (backend)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

### Quick start (frontend)

```bash
npm install
npm run build
```

## License

By contributing you agree that your contributions will be licensed under the [MIT License](LICENSE).
