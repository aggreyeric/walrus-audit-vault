# Contributing to Walrus Audit Vault

Thanks for your interest in contributing! 🦭 This project is built for the
[Sui Overflow 2026 — Walrus Track](https://overflow.sui.io), and we welcome
contributions that make the audit vault more robust, verifiable, and useful.

## 📋 Table of Contents

- [Development Setup](#-development-setup)
- [Installing Dependencies](#-installing-dependencies)
- [Running Tests](#-running-tests)
- [Code Style](#-code-style)
- [Pull Request Process](#-pull-request-process)
- [Reporting Issues](#-reporting-issues)

---

## 🛠 Development Setup

Requirements:

- **Python 3.11+** (required — `requires-python = ">=3.11"`)
- **git**
- (Optional) a Sui wallet address and Walrus testnet access, only needed if
  you're testing live store/verify flows.

Fork & clone the repo:

```bash
git clone https://github.com/your-username/walrus-audit-vault.git
cd walrus-audit-vault
git remote add upstream https://github.com/aggreyeric/walrus-audit-vault.git
```

## 📦 Installing Dependencies

We recommend an isolated virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
```

Install the package **and** development dependencies in editable mode:

```bash
pip install -e ".[dev]"
```

This installs:

- Runtime deps: `httpx`, `pydantic`
- Dev deps: `pytest>=8.0`

## ✅ Running Tests

The test suite lives in `tests/` and is configured via `pyproject.toml`
(`testpaths = ["tests"]`, quiet output).

Run the full suite:

```bash
pytest tests/
```

Run a single file or test:

```bash
pytest tests/test_store.py
pytest tests/test_store.py::test_store_blob
```

With coverage (if you add `pytest-cov`):

```bash
pytest tests/ --cov=walrus_audit_vault
```

> 💡 Tests run against the public Walrus testnet publisher/aggregator.
> Network-dependent tests should be marked and skipped gracefully if the
> network is unavailable.

## 🧹 Code Style

- Follow existing style — keep modules small and focused.
- Type hints are encouraged (we use `pydantic` models for data shapes).
- Keep functions pure where possible (especially hashing/signing logic).
- Every new feature or bug fix should ship with a test.

## 🔄 Pull Request Process

1. **Sync with upstream** before starting work:
   ```bash
   git checkout main
   git pull upstream main
   ```
2. **Create a feature branch** off `main`:
   ```bash
   git checkout -b feat/short-description
   ```
   Use conventional prefixes: `feat/`, `fix/`, `docs/`, `test/`, `refactor/`.
3. **Make your changes.** Keep commits atomic and write clear commit messages
   (we follow [Conventional Commits](https://www.conventionalcommits.org/),
   e.g. `feat: anchor blob id on Sui registry`).
4. **Run the tests** and make sure they pass:
   ```bash
   pytest tests/
   ```
5. **Push to your fork** and open a Pull Request against `main`:
   ```bash
   git push -u origin feat/short-description
   ```
6. **Fill in the PR template** (if present). Your PR description should cover:
   - **What** changed and **why**
   - **How** it was tested (commands + output if relevant)
   - Any **breaking changes** or migration notes
7. **Request review.** A maintainer will review, request changes if needed,
   and squash-merge once approved.
8. **Keep your branch updated** with `main` during review:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

### PR Checklist

- [ ] Branch is named with a conventional prefix
- [ ] `pytest tests/` passes locally
- [ ] New code has tests
- [ ] No secrets or private keys committed
- [ ] README/docs updated if behavior changed
- [ ] Commit messages follow Conventional Commits

## 🐛 Reporting Issues

Open a [GitHub Issue](https://github.com/aggreyeric/walrus-audit-vault/issues)
with:

- What you expected to happen
- What actually happened (logs / error output)
- Steps to reproduce
- Your environment (Python version, OS, whether on testnet/mainnet)

---

By contributing, you agree that your contributions will be licensed under the
[MIT License](./LICENSE).
