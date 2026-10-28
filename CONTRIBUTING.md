# Contributing to Simple Graphics

Thank you for helping improve Simple Graphics, a beginner-friendly Python graphics library.

## Getting Started

1. Fork the repository and clone your fork.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows, activate it with:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install the project in editable mode:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -e .
   ```

4. Make your changes in a separate branch.

## Making Changes

- Keep the public API readable and beginner-friendly.
- Prefer small, focused changes that match the existing style.
- Update the README when changing public behavior or adding a feature.
- Add or update an example in `examples/` when it helps demonstrate a user-facing feature.
- Do not commit generated files, virtual environments, build output, or local editor settings.
- Keep compatibility with Python 3.9 and newer unless the project requirements are intentionally changed.

## Running Examples

Examples use Pygame and open a window. From the repository root, run an example with:

```bash
python examples/mouse_circle.py
```

Close the window to stop the program. Other examples are available in `examples/`.

## Checking Your Changes

Before opening a pull request:

- Run the example or workflow affected by your change.
- Format your changes:
  ```bash
  ruff format
  ```
- Check that the package imports correctly:

  ```bash
  python -c "import simple_graphics; print('Import succeeded')"
  ```

- Compile the Python source and examples to catch syntax errors:

  ```bash
  python -m compileall src examples
  ```

- Review the diff and remove unrelated changes.

If you add automated tests, keep them focused on observable library behavior and ensure they can run without requiring a display where possible.

## Pull Requests

Pull requests should include:

- A concise description of the problem and solution.
- The commands or examples used to validate the change.
- Documentation or example updates for public API changes.
- Screenshots or a short recording for visible graphics changes, when useful.

Please keep each pull request focused on one feature or fix. Maintainers may request changes to improve clarity, compatibility, or consistency with the library's educational goals.

## Reporting Issues

When opening an issue, include:

- Your operating system and Python version.
- The installed Simple Graphics version or commit.
- A minimal example that reproduces the problem.
- The full error message and traceback, if one is available.
- What you expected to happen and what happened instead.

For security-sensitive reports, please avoid posting exploitable details publicly until maintainers have had an opportunity to respond.

## License

By contributing, you agree that your contributions may be distributed under the project's [MIT License](LICENSE).
