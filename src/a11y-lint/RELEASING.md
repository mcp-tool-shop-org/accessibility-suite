# Releasing a11y-lint

## Pre-Release Checklist

Before tagging a release:

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Type checks pass (`pyright`)
- [ ] CLI output contract unchanged (or major version bump)
- [ ] Schema version unchanged (or major version bump)
- [ ] No regressions in accessibility findings
- [ ] README updated with any new features
- [ ] RELEASE_NOTES.md updated

---

## Release Process

1. **Update version** in `pyproject.toml`
2. **Update RELEASE_NOTES.md** with changes
3. **Run full test suite**:
   ```bash
   pytest tests/ -v
   ```
4. **Create git tag**:
   ```bash
   git tag -a v0.x.x -m "Release v0.x.x"
   git push origin v0.x.x
   ```
5. **Create GitHub release** with release notes
6. **Publish to PyPI**:
   ```bash
   python -m build
   twine upload dist/*
   ```

---

## Release Blockers

The following block releases:

- Failing tests
- Accessibility regressions
- Breaking changes without major version bump
- Schema changes without major version bump

---

## Hotfix Process

For critical bugs:

1. Create branch from latest release tag
2. Fix the issue with minimal changes
3. Add regression test
4. Tag as patch release (e.g., v0.1.1)
