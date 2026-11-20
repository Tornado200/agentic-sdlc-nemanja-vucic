# 11. Risks and Technical Debt

## 11.1 Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Over-engineering** | Medium | High | Start with simplest solution. Defer complex patterns until proven necessary. |
| **State management complexity** | Low | Medium | In-memory state only. No persistence in initial scope. Clear module boundaries. |
| **Testing gaps in navigation logic** | Medium | High | Comprehensive unit tests with property-based testing for edge cases. |
| **CLI argument parsing errors** | Low | Low | Use argparse with validation. Clear error messages for malformed inputs. |

## 11.2 Technical Debt

**Accepted Technical Debt:**
1. **No error recovery**: Failed commands require complete restart.
   - *Reason*: Simplicity for kata scope.
   - *Future*: Could add checkpoint/resume feature.

2. **Hardcoded obstacle configuration**:
   - *Reason*: Minimize initial complexity.
   - *Future*: External configuration file support.

**Monitoring:** Technical debt tracked in project issues. No immediate action required for kata completion.

---

*Next: Chapter 12 will provide the glossary.*
