# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- ================================================================
HOW TO UPDATE THIS FILE:
  1. Every PR that changes user-facing behavior MUST update [Unreleased].
  2. At release time, rename [Unreleased] to [X.Y.Z] - YYYY-MM-DD.
  3. Create a new empty [Unreleased] section at the top.

CATEGORIES (use only the ones that apply):
  - Added:      New features
  - Changed:    Changes in existing functionality
  - Deprecated: Features that will be removed in future versions
  - Removed:    Features removed in this version
  - Fixed:      Bug fixes
  - Security:   Vulnerability fixes

VERSIONING RULES (Semantic Versioning):
  - MAJOR (X.0.0): Breaking changes to public API
  - MINOR (0.X.0): New functionality, backward compatible
  - PATCH (0.0.X): Bug fixes, backward compatible
================================================================ -->

## [Unreleased]

### Added

- _Nothing yet._

### Changed

- _Nothing yet._

---

## [1.2.0] - 2026-03-01

### Added

- `TimeSeriesFeatureEngine` class for automated feature generation ([#45](https://github.com/org/project/pull/45)).
- Support for custom rolling window functions via `rolling_fn` parameter ([#48](https://github.com/org/project/pull/48)).
- Data dictionary for `sales_daily` dataset ([#50](https://github.com/org/project/pull/50)).

### Changed

- `add_lag_features()` now supports grouped computation via `group_columns` parameter ([#46](https://github.com/org/project/pull/46)).
- Updated minimum Python version to 3.11 ([#47](https://github.com/org/project/pull/47)).
- Improved memory efficiency of rolling statistics by 40% ([#49](https://github.com/org/project/pull/49)).

### Deprecated

- `compute_lags()` — use `add_lag_features()` instead. Will be removed in v2.0.0 ([#46](https://github.com/org/project/pull/46)).

### Fixed

- Memory leak in rolling statistics computation with large windows ([#142](https://github.com/org/project/issues/142)).
- Incorrect lag values when DataFrame index was not sorted ([#138](https://github.com/org/project/issues/138)).

---

## [1.1.0] - 2026-02-01

### Added

- `validate_dataframe()` utility function for data quality checks.
- Pre-commit hooks configuration with black, isort, and ruff.
- MkDocs documentation with auto-generated API reference.

### Changed

- Migrated from `setup.py` to `pyproject.toml`.
- Standardized all docstrings to Google Style.

### Fixed

- Type annotations now use PEP 604 syntax (`X | None` instead of `Optional[X]`).

---

## [1.0.0] - 2026-01-15

### Added

- Initial release.
- `add_lag_features()` function for creating lag features.
- `add_rolling_features()` function for rolling statistics.
- Basic data loading utilities.
- Unit and integration tests with 85% coverage.
- README, CONTRIBUTING, and LICENSE files.

---

<!-- Link definitions -->
[Unreleased]: https://github.com/org/project/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/org/project/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/org/project/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/org/project/releases/tag/v1.0.0
