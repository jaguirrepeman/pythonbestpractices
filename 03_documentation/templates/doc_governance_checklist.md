# Documentation Governance Checklist

> **Purpose:** Ensure documentation stays accurate, complete, and current throughout the project lifecycle.  
> **Frequency:** Review this checklist at every PR, sprint review, and release.

---

## Per-PR Checklist (Every Pull Request)

### In-Code Documentation

- [ ] All **new** public functions/classes have Google Style docstrings
- [ ] All **modified** public functions/classes have updated docstrings
- [ ] Type hints are complete and match docstring types
- [ ] Docstrings include at least one `Example` for complex functions
- [ ] `Raises` section documents all exceptions
- [ ] `pydocstyle --convention=google` passes without errors
- [ ] `interrogate` reports ≥ 95% docstring coverage
- [ ] Inline comments explain **why**, not **what**

### Off-Code Documentation

- [ ] README updated if the change affects usage, installation, or configuration
- [ ] CHANGELOG updated under `[Unreleased]` section
- [ ] API documentation builds without warnings (`mkdocs build --strict`)
- [ ] Data dictionary updated if schema changes were made
- [ ] ADR created if a significant architectural decision was made

---

## Weekly Review Checklist

| Check | Responsible | Done |
|-------|-------------|------|
| Review `interrogate` coverage trend (should be stable or increasing) | Tech Lead | ☐ |
| Scan for TODO/FIXME comments older than 2 sprints | Any dev | ☐ |
| Verify CI doc checks are green on main branch | Tech Lead | ☐ |
| Check for open PRs with "docs-needed" label | Doc Owner | ☐ |

---

## Monthly Audit Checklist

| Check | Responsible | Done |
|-------|-------------|------|
| Run full `mkdocs build --strict` and fix all warnings | Doc Owner | ☐ |
| Review README for accuracy (links, versions, instructions) | Tech Lead | ☐ |
| Audit data dictionaries against current schemas | Data Engineering | ☐ |
| Check wiki pages for stale/outdated content | All team | ☐ |
| Review and update onboarding documentation | Tech Lead | ☐ |
| Verify all runbooks match current deployment process | Platform Team | ☐ |
| Check that all deprecated items have migration docs | Senior Eng | ☐ |

---

## Per-Release Checklist

### Before release

- [ ] CHANGELOG `[Unreleased]` section renamed to `[X.Y.Z] - YYYY-MM-DD`
- [ ] New `[Unreleased]` section created
- [ ] All deprecated items documented with removal timeline
- [ ] Migration guide written for breaking changes (major releases)
- [ ] API reference regenerated and verified
- [ ] README version badge updated
- [ ] Release notes drafted from CHANGELOG entries

### After release

- [ ] Documentation deployed for new version (`mike deploy X.Y.Z`)
- [ ] `latest` alias updated to point to new version
- [ ] Release notes published on GitHub/GitLab
- [ ] Team notified of documentation updates
- [ ] Wiki updated with release-specific information

---

## Roles & Responsibilities

| Role | Responsibilities |
|------|-----------------|
| **Developer** | Write docstrings, update README, update CHANGELOG per PR |
| **Reviewer** | Verify documentation completeness during code review |
| **Tech Lead** | Weekly coverage review, monthly audit, release docs |
| **Doc Owner** | Monthly audit, wiki maintenance, standards enforcement |
| **Data Engineering** | Data dictionary maintenance, pipeline documentation |
| **Platform Team** | CI/CD docs, runbook maintenance |

---

## Metrics to Track

| Metric | Target | Tool |
|--------|--------|------|
| Docstring coverage | ≥ 95% | `interrogate` |
| MkDocs build warnings | 0 | `mkdocs build --strict` |
| Pydocstyle violations | 0 | `pydocstyle --convention=google` |
| README last updated | < 30 days | Git log |
| Open "docs-needed" issues | < 5 | GitHub labels |
| Data dictionary freshness | Updated within 1 sprint of schema change | Manual review |

---

## Automation Setup

### Required CI checks (blocking merge)

```yaml
# These checks MUST pass before a PR can be merged
- pydocstyle --convention=google src/
- interrogate -v src/ --fail-under=95
- mkdocs build --strict
```

### Recommended CI checks (non-blocking, informational)

```yaml
# These generate warnings but don't block merge
- interrogate -v src/ --fail-under=100  # Aspirational 100% coverage
- codespell docs/ src/                   # Spell checker
```

### GitHub labels for documentation tracking

| Label | Color | Description |
|-------|-------|-------------|
| `docs-needed` | 🟡 yellow | PR needs documentation updates |
| `docs-updated` | 🟢 green | Documentation has been updated |
| `docs-only` | 🔵 blue | PR contains only documentation changes |
| `breaking-change` | 🔴 red | Requires migration guide |

---

## Escalation Process

1. **Reviewer finds missing docs in PR** → Requests changes, adds `docs-needed` label
2. **CI check fails for docs** → PR cannot be merged until fixed
3. **Monthly audit finds stale docs** → Create issue, assign to doc owner
4. **Critical runbook is outdated** → Escalate to Tech Lead, fix within 48h
5. **Data dictionary doesn't match schema** → Block data pipeline changes until updated
