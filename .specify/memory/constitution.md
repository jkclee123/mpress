<!--
Sync Impact Report:
Version change: 1.0.0 → 1.0.1 (tooling constraint addition)
Principles modified: None
Sections modified:
  - Additional Constraints (added uv requirement)
Templates requiring updates:
  ✅ plan-template.md (no changes needed)
  ✅ spec-template.md (no changes needed)
  ✅ tasks-template.md (no changes needed)
Follow-up TODOs: None
-->

# mpress Constitution

## Core Principles

### I. Code Quality

All code MUST adhere to strict quality standards to ensure maintainability,
reliability, and readability. Code MUST be self-documenting with clear naming
conventions, appropriate comments for complex logic, and consistent formatting.
All functions and modules MUST have single, well-defined responsibilities.
Code MUST pass static analysis tools (linters, type checkers) with zero
warnings before merge. Code reviews MUST verify adherence to these standards.
Refactoring is encouraged when code quality degrades, and technical debt MUST
be documented and tracked.

**Rationale**: High code quality reduces bugs, accelerates development velocity,
and ensures the codebase remains maintainable as the project grows. Consistent
standards enable team collaboration and reduce cognitive load.

### II. Testing Standards (NON-NEGOTIABLE)

Test-Driven Development (TDD) is mandatory for all new features: Tests MUST
be written and approved before implementation begins. Tests MUST fail initially,
then implementation proceeds through the Red-Green-Refactor cycle. All user
stories MUST have corresponding acceptance tests that verify the complete user
journey. Unit tests MUST cover core business logic with minimum 80% code
coverage. Integration tests MUST verify end-to-end workflows for each supported
media format. Edge cases identified in specifications MUST have explicit test
cases. Tests MUST be deterministic, isolated, and runnable independently.
Test failures MUST block merges until resolved.

**Rationale**: Comprehensive testing prevents regressions, documents expected
behavior, and provides confidence when refactoring. TDD ensures requirements
are understood before implementation and catches defects early.

### III. User Experience Consistency

The command-line interface MUST provide consistent, predictable behavior across
all operations. Error messages MUST be clear, actionable, and indicate the
specific problem encountered. Success feedback MUST be provided when operations
complete. The tool MUST handle edge cases gracefully without crashing or
corrupting user data. File operations MUST be atomic: either the compression
succeeds and replaces the original, or the original file remains unchanged.
The tool MUST preserve file metadata (format, location) as specified in
requirements. Command-line argument parsing MUST be consistent and follow
standard Unix conventions.

**Rationale**: Consistent UX reduces user confusion, builds trust, and ensures
the tool is reliable for production use. Predictable behavior enables users to
develop workflows around the tool.

### IV. Performance Requirements

The tool MUST process files efficiently without excessive memory consumption.
Compression operations MUST complete within reasonable timeframes for typical
file sizes (small images < 1 second, large videos < 5 minutes for 1GB files).
Memory usage MUST remain bounded and not grow linearly with file size for
streaming-capable operations. The tool MUST handle concurrent file processing
without deadlocks or race conditions. Performance benchmarks MUST be established
for each supported media format and maintained as acceptance criteria. Large
file handling MUST use streaming or chunked processing to avoid memory
exhaustion.

**Rationale**: Performance directly impacts user productivity and system
resource utilization. Efficient processing enables batch operations and ensures
the tool remains usable on systems with limited resources.

## Additional Constraints

The tool MUST operate exclusively on macOS and leverage platform-specific
optimizations where beneficial. All dependencies MUST be clearly documented
and version-pinned. The tool MUST support the specified media formats (PNG,
JPG, JPEG, MOV, MP4, WebM) with format preservation. Compression algorithms
MUST balance file size reduction with quality preservation appropriate for
each media type. The tool MUST not require user configuration or settings files.

For Python projects, Python MUST always be executed using `uv run` and packages
MUST be installed using `uv pip`. Direct `python` or `pip` commands are
prohibited. This ensures consistent dependency management and reproducible
environments across all development and CI/CD workflows.

## Development Workflow

All code changes MUST undergo peer review before merge. Pull requests MUST
include tests that verify the changes. Code reviews MUST verify constitution
compliance, including code quality standards, test coverage, UX consistency,
and performance considerations. Continuous integration MUST run all tests and
static analysis tools, and failures MUST block merges. Documentation MUST be
updated when features are added or behavior changes. Breaking changes MUST be
documented with migration guides.

## Governance

This constitution supersedes all other development practices and guidelines.
Amendments to principles require documentation of rationale, impact assessment,
and approval. Version changes follow semantic versioning: MAJOR for
backward-incompatible changes, MINOR for new principles or sections, PATCH
for clarifications. All pull requests and code reviews MUST verify compliance
with constitution principles. Complexity additions MUST be justified with
explicit rationale when they conflict with simplicity goals.

**Version**: 1.0.1 | **Ratified**: 2025-01-27 | **Last Amended**: 2025-01-27
