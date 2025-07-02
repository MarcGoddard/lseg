# Clean Up Checklist for Version 1 Application

1. [ ] Remove old v1 scripts (`log_monitor.py`, `test_log_monitor.py`) from the repo root.
2. [ ] Remove any old test log files (e.g., `test_logs.log`, `empty.log`) not needed for v2.
3. [ ] Remove or archive any old documentation referencing v1 (e.g., `OLD_README.md`).
4. [ ] Clean up `.pyc` files and `__pycache__` directories throughout the repo.
5. [ ] Update `.gitignore` to include `.pyc`, `__pycache__/`, and any output files not to be tracked.
6. [ ] Tag the last v1 commit in git (e.g., `git tag v1.2.0`).
7. [ ] Confirm all v2 tests pass and the modular app runs as expected.
8. [ ] Update all documentation to reference only the v2 structure and usage.
9. [ ] Remove any duplicate or unused dependencies from `requirements.txt`.
10. [ ] Notify collaborators of the new structure and clean-up.

---
For automated cleanup, see `cleanup_v1.ps1` in the project root.
