# CipherForge Agent Guidelines

These instructions apply to coding agents working anywhere in this repository.
Use `README.md` for the project overview, `CONTRIBUTING.md` for contributor
setup and workflow, and `SECURITY.md` for the full security policy.

## Project Purpose and Safety

- CipherForge is an educational and experimental cryptography toolkit, not a
  production security library. Its implementations are unaudited and may lack
  constant-time behavior, memory clearing, or complete validation.
- Preserve the educational purpose. Clearly label broken, deprecated,
  experimental, or insecure algorithms and demonstrations; do not imply they
  are suitable for protecting real data.
- Do not add real credentials, production keys, private certificates, or other
  secrets. Use clearly synthetic examples and test fixtures.
- Treat cryptographic correctness carefully. Prefer established specifications
  and cite the relevant RFC, NIST publication, or other primary reference in
  documentation when applicable. Do not claim conformance without appropriate
  tests.

## Repository Structure

- `level-01-classical-ciphers/` through `level-08-capstone-project/` contain
  the learning modules, grouped by curriculum level.
- `main.py` provides the interactive CLI and module diagnostics/registration.
- `tests/` contains the pytest suite.
- Each level and selected subdirectories have READMEs with local learning
  material. Check the relevant README before changing a module.
- Keep a module self-contained and follow nearby implementations. Interactive
  modules should expose the expected `{name}_menu()` entry point and be
  registered in `main.py` and the appropriate level menu when required.

## Before Editing

- Inspect the relevant implementation, callers, tests, and documentation
  before changing behavior. Search for existing helpers and patterns first.
- Keep changes focused on the request. Avoid unrelated refactors or broad
  formatting changes.
- Preserve compatibility with Python 3.10 and later; do not introduce syntax
  or standard-library APIs unavailable at the project's minimum version.
- Prefer clear, typed Python that matches the surrounding code. Handle invalid
  input explicitly and avoid silent fallbacks that hide errors.
- When validating hashes, tokens, or MAC tags, use
  `secrets.compare_digest()` or `hmac.compare_digest()` as appropriate.

## Tests and Validation

- Add or update tests for behavior changes, boundary conditions, and relevant
  invalid inputs. Use known-answer vectors from the applicable specification
  for algorithm implementations when available.
- Run the narrowest relevant tests first. Run the full suite when practical:
  `pytest tests/ -v`
- Run module diagnostics when changes affect imports, module registration, or
  the interactive application:
  `python -c "import main, sys; ok, fail = main.run_diagnostics(pause=False); sys.exit(fail)"`
- The CI workflow tests Python 3.10–3.13 on Ubuntu and Windows; use
  `.github/workflows/ci.yml` as the source of truth for CI commands and matrix.
- Report exactly which checks were run and their outcomes. Distinguish a
  failed check from one that could not run because of environment/dependency
  issues. Never claim unrun tests passed.

## Documentation

- Update relevant level/module documentation when user-visible behavior,
  interfaces, limitations, or educational explanations change.
- Explain security limitations and assumptions. Do not present heuristic
  rankings as probabilities or confidence unless they are actually calibrated.
- Avoid duplicating material already maintained in `README.md`,
  `CONTRIBUTING.md`, or `SECURITY.md`; link to those documents instead.

## Git and Pull Requests

- Make changes on a dedicated feature or fix branch, not directly on `main`.
  If the current branch is `main`, create a task branch before editing.
- Preserve existing user changes. Do not switch branches if doing so could
  lose or mix unrelated work; ask the user how to proceed.
- Do not commit, push, merge, or delete branches unless the user explicitly
  asks. Never force push.
- Keep each pull request focused. Use
  `.github/PULL_REQUEST_TEMPLATE.md`, preserving its sections and checklist,
  and include relevant test evidence.
