# Architecture Overview

This document provides a technical overview of the DGW Scrapper architecture and implementation details.

## Table of Contents

- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Code Structure](#code-structure)
- [Data Flow](#data-flow)
- [Key Components](#key-components)
- [Design Decisions](#design-decisions)

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       DGW Scrapper                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐   ┌──────────────┐  │
│  │  CLI Input   │───▶│   Browser    │──▶│    Data      │  │
│  │  (argparse)  │    │  Automation  │   │  Processing  │  │
│  │              │    │ (Playwright) │   │  (pandas)    │  │
│  └──────────────┘    └──────────────┘   └──────────────┘  │
│         │                    │                   │          │
│         ▼                    ▼                   ▼          │
│  ┌──────────────┐    ┌──────────────┐   ┌──────────────┐  │
│  │ Credentials  │    │  Web Pages   │   │    Excel     │  │
│  │  Validation  │    │  Navigation  │   │   Export     │  │
│  └──────────────┘    └──────────────┘   └──────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Core Dependencies

| Technology | Version | Purpose             |
| ---------- | ------- | ------------------- |
| Python     | 3.8+    | Primary language    |
| Playwright | 1.30.0+ | Browser automation  |
| Pandas     | 2.0.0+  | Data manipulation   |
| Rich       | 13.0.0+ | Terminal UI         |
| openpyxl   | 3.1.0+  | Excel file handling |
| lxml       | 5.0.0+  | HTML parsing        |

### Development Tools

- Git for version control
- GitHub for repository hosting
- VS Code (recommended IDE)

## Code Structure

```
dgw-scrapper/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── output/                 # Generated Excel files (gitignored)
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # Contribution guidelines
├── CHANGELOG.md           # Version history
├── SECURITY.md            # Security policy
├── CODE_OF_CONDUCT.md     # Community guidelines
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    └── pull_request_template.md
```

## Data Flow

### 1. Input Phase

```python
# User provides credentials and date range
--email user@example.com
--password password123
--from_date 01/01/2024
--to_date 31/01/2024
```

### 2. Authentication Phase

```
User Input → Credential Sanitization → Browser Launch → Login → Session
```

### 3. Navigation Phase

```
Home → Inbox → Sudah Diproses Tab → Apply Filters → Search Results
```

### 4. Data Extraction Phase

```
For each LPJ item:
  Extract Metadata → Open Document → Parse Table → Clean Data
```

### 5. Processing Phase

```
Raw Data → Column Removal → Text Cleaning → Type Conversion → Aggregation
```

### 6. Output Phase

```
Processed DataFrame → Excel File → Save to output/ directory
```

## Key Components

### 1. Command-Line Interface (CLI)

**File**: `main.py` (lines 52-62)

```python
parser = argparse.ArgumentParser(...)
parser.add_argument('--email', required=True, ...)
parser.add_argument('--password', required=True, ...)
parser.add_argument('--from_date', required=True, ...)
parser.add_argument('--to_date', required=True, ...)
```

**Responsibilities**:

- Parse command-line arguments
- Validate input format
- Provide help documentation

### 2. Browser Automation

**File**: `main.py` (lines 71-85)

```python
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
```

**Responsibilities**:

- Manage browser lifecycle
- Handle page navigation
- Interact with web elements
- Wait for page loads

### 3. Date Picker Navigation

**File**: `main.py` (lines 95-125)

```python
while True:
    current_calendar = page.locator("...").inner_text()
    current_datetime = datetime.strptime(current_calendar, "%B %Y")
    # Navigate to correct month/year
```

**Responsibilities**:

- Navigate calendar interface
- Select specific dates
- Handle month/year transitions

### 4. Data Extraction

**File**: `main.py` (lines 163-175)

```python
table_locator = page.get_by_role("table", name="activity table").last
table_html = table_locator.evaluate("el => el.outerHTML")
df = pd.read_html(StringIO(table_html))[0]
```

**Responsibilities**:

- Locate HTML tables
- Extract table data
- Convert to DataFrame

### 5. Data Transformation

**File**: `main.py` (lines 177-206)

```python
# Remove unnecessary columns
df = df.drop(columns=[...])

# Clean text
df['Activity Name'] = df['Activity Name'].str.replace(...)

# Convert currency to numbers
df['Total'] = df['Total'].astype(str).str.replace(...).astype('int64')

# Aggregate
df = df.groupby([...]).agg(...)
```

**Responsibilities**:

- Clean column data
- Type conversion
- Data aggregation
- Format standardization

### 6. Error Handling

**File**: `main.py` (lines 209-212)

```python
except TimeoutError:
    logger.warning(f"TimeoutError for item {index+1}: {filename}")
    continue
```

**Responsibilities**:

- Handle network timeouts
- Skip problematic items
- Log errors
- Continue processing

## Design Decisions

### 1. Playwright over Selenium

**Rationale**:

- Faster execution
- Better async support
- More reliable selectors
- Modern API design

### 2. Pandas for Data Processing

**Rationale**:

- Powerful data manipulation
- Built-in aggregation functions
- Easy Excel export
- Industry standard

### 3. Rich for Terminal UI

**Rationale**:

- Beautiful progress bars
- Colored logging
- Improved user experience
- Minimal configuration

### 4. Synchronous Execution

**Rationale**:

- Simpler code
- Easier debugging
- Sequential processing is acceptable for this use case
- Avoids race conditions

### 5. Single File Architecture

**Rationale**:

- Simple deployment
- Easy to understand
- No module complexity
- Suitable for script-sized application

### 6. Headless Browser

**Rationale**:

- Faster execution
- Server compatibility
- Resource efficient
- No GUI dependencies

## Performance Considerations

### Optimization Strategies

1. **Network Waits**: Use `networkidle` to ensure complete page loads
2. **Element Waits**: Wait for specific elements before interaction
3. **Batch Processing**: Process all items in single browser session
4. **Lazy Evaluation**: Only extract needed data

### Scalability

Current implementation handles:

- ✅ Small datasets (< 100 items): Excellent
- ✅ Medium datasets (100-500 items): Good
- ⚠️ Large datasets (> 500 items): May need optimization

### Potential Improvements

1. **Parallel Processing**: Process multiple items concurrently
2. **Resume Capability**: Save progress and resume interrupted sessions
3. **Caching**: Cache authentication and navigation state
4. **Database Storage**: Store data in database instead of files

## Error Handling Strategy

### Error Types

| Error Type       | Handling  | Recovery                  |
| ---------------- | --------- | ------------------------- |
| Login failure    | Abort     | User must fix credentials |
| Network timeout  | Skip item | Continue with next        |
| Missing data     | Skip item | Log warning               |
| File write error | Abort     | User must fix permissions |

### Logging Levels

- **INFO**: Normal operations
- **WARNING**: Recoverable errors
- **ERROR**: Critical failures (currently not implemented)

## Security Considerations

1. **Credential Handling**: Sanitized but passed via CLI (insecure for production)
2. **Output Protection**: Files stored locally without encryption
3. **Browser Security**: Uses Chromium security features
4. **No Input Validation**: Trusts web page data structure

See [SECURITY.md](SECURITY.md) for detailed security guidelines.

## Future Enhancements

### Planned Features

- [ ] Configuration file support (YAML/JSON)
- [ ] Multiple document type support
- [ ] Export format options (CSV, JSON, SQLite)
- [ ] Resume interrupted sessions
- [ ] Parallel processing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Docker containerization
- [ ] Web API endpoint
- [ ] Scheduled execution

### Architecture Evolution

```
Current: Monolithic Script
    ↓
Phase 1: Modular Structure
    ↓
Phase 2: Config-driven
    ↓
Phase 3: API Service
    ↓
Phase 4: Distributed System
```

## Contributing to Architecture

When proposing architectural changes:

1. Open an issue describing the change
2. Discuss trade-offs and alternatives
3. Update this document
4. Implement with tests
5. Update relevant documentation

---

Last Updated: October 27, 2025
