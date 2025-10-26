# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features

- Support for additional document types
- Configuration file support
- Resume capability for interrupted scraping sessions
- Export to multiple formats (CSV, JSON)

## [1.0.0] - 2025-10-27

### Added

- Initial release
- Automated login to DGW Spartan platform
- Date range filtering for LPJ documents
- Excel export with cleaned and aggregated data
- Rich terminal interface with progress tracking
- Automatic output directory management
- Error handling for timeout issues
- Batch processing of multiple documents

### Features

- Command-line interface with argparse
- Playwright-based browser automation
- Pandas-based data processing and aggregation
- Rich logging with progress bars
- Automatic file naming based on document metadata

### Dependencies

- playwright >= 1.30.0
- pandas >= 2.0.0
- rich >= 13.0.0
- openpyxl >= 3.1.0
- lxml >= 5.0.0

---

## Legend

- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities
