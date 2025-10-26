# Example Usage Guide

This document provides detailed examples of how to use DGW Scrapper in various scenarios.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Common Scenarios](#common-scenarios)
- [Advanced Usage](#advanced-usage)
- [Tips and Tricks](#tips-and-tricks)
- [Troubleshooting Examples](#troubleshooting-examples)

## Basic Usage

### Single Month Data Extraction

Extract data for January 2024:

```bash
python main.py \
  --email user@example.com \
  --password mypassword123 \
  --from_date 01/01/2024 \
  --to_date 31/01/2024
```

### Single Day Data Extraction

Extract data for a specific day:

```bash
python main.py \
  --email user@example.com \
  --password mypassword123 \
  --from_date 15/03/2024 \
  --to_date 15/03/2024
```

## Common Scenarios

### Scenario 1: Monthly Report

Extract a full month of data:

```bash
# January 2024
python main.py \
  --email finance@company.com \
  --password SecurePass123! \
  --from_date 01/01/2024 \
  --to_date 31/01/2024
```

**Expected Output:**

- Multiple Excel files in `output/` directory
- Files named: `2024 - January - [Submitter] - [Activity Type] - [Proposal].xlsx`

### Scenario 2: Quarterly Report

For quarterly data, run the command for each month:

```bash
# Q1 2024 - January
python main.py --email user@example.com --password pass --from_date 01/01/2024 --to_date 31/01/2024

# Q1 2024 - February
python main.py --email user@example.com --password pass --from_date 01/02/2024 --to_date 29/02/2024

# Q1 2024 - March
python main.py --email user@example.com --password pass --from_date 01/03/2024 --to_date 31/03/2024
```

### Scenario 3: Year-End Report

For annual data, process month by month:

```bash
#!/bin/bash
# Script to extract entire year data

EMAIL="user@example.com"
PASSWORD="mypassword"
YEAR="2024"

# Array of month data (days in each month)
declare -a MONTHS=(
    "01/01 31/01"  # January
    "01/02 29/02"  # February (leap year)
    "01/03 31/03"  # March
    "01/04 30/04"  # April
    "01/05 31/05"  # May
    "01/06 30/06"  # June
    "01/07 31/07"  # July
    "01/08 31/08"  # August
    "01/09 30/09"  # September
    "01/10 31/10"  # October
    "01/11 30/11"  # November
    "01/12 31/12"  # December
)

for month_range in "${MONTHS[@]}"; do
    FROM=$(echo $month_range | cut -d' ' -f1)
    TO=$(echo $month_range | cut -d' ' -f2)

    echo "Processing: $FROM/$YEAR to $TO/$YEAR"

    python main.py \
        --email "$EMAIL" \
        --password "$PASSWORD" \
        --from_date "$FROM/$YEAR" \
        --to_date "$TO/$YEAR"

    # Optional: Add delay between requests
    sleep 5
done

echo "Annual data extraction complete!"
```

## Advanced Usage

### Using Environment Variables

Create a `.env` file (⚠️ Never commit this file!):

```bash
# .env
DGW_EMAIL=user@example.com
DGW_PASSWORD=mypassword123
```

Then use it in your commands:

```bash
# Load environment variables
source .env

# Run the scraper
python main.py \
  --email "$DGW_EMAIL" \
  --password "$DGW_PASSWORD" \
  --from_date 01/01/2024 \
  --to_date 31/01/2024
```

### Bash Script for Repeated Use

Create `run_scraper.sh`:

```bash
#!/bin/bash

# Load credentials from environment
if [ -f ".env" ]; then
    source .env
else
    echo "Error: .env file not found"
    exit 1
fi

# Get date range from arguments or use defaults
FROM_DATE=${1:-"01/01/2024"}
TO_DATE=${2:-"31/01/2024"}

echo "Running DGW Scrapper..."
echo "From: $FROM_DATE"
echo "To: $TO_DATE"

python main.py \
    --email "$DGW_EMAIL" \
    --password "$DGW_PASSWORD" \
    --from_date "$FROM_DATE" \
    --to_date "$TO_DATE"

echo "Complete! Check output/ directory for results."
```

Make it executable:

```bash
chmod +x run_scraper.sh
```

Use it:

```bash
# Use default dates
./run_scraper.sh

# Specify custom dates
./run_scraper.sh 01/02/2024 28/02/2024
```

### Windows Batch Script

Create `run_scraper.bat`:

```batch
@echo off
setlocal

REM Load credentials from environment variables
if not defined DGW_EMAIL (
    echo Error: DGW_EMAIL environment variable not set
    exit /b 1
)

if not defined DGW_PASSWORD (
    echo Error: DGW_PASSWORD environment variable not set
    exit /b 1
)

REM Get date range from arguments or use defaults
set FROM_DATE=%1
set TO_DATE=%2

if "%FROM_DATE%"=="" set FROM_DATE=01/01/2024
if "%TO_DATE%"=="" set TO_DATE=31/01/2024

echo Running DGW Scrapper...
echo From: %FROM_DATE%
echo To: %TO_DATE%

python main.py ^
    --email %DGW_EMAIL% ^
    --password %DGW_PASSWORD% ^
    --from_date %FROM_DATE% ^
    --to_date %TO_DATE%

echo Complete! Check output directory for results.
pause
```

## Tips and Tricks

### 1. Processing Large Date Ranges

**Problem**: Need to process 6 months of data.

**Solution**: Break it into monthly batches:

```bash
# Process each month separately to avoid timeouts
for month in {1..6}; do
    FROM_DATE=$(date -d "2024-$month-01" +%d/%m/%Y)
    TO_DATE=$(date -d "2024-$month-01 +1 month -1 day" +%d/%m/%Y)

    echo "Processing month $month: $FROM_DATE to $TO_DATE"
    python main.py --email user@example.com --password pass --from_date "$FROM_DATE" --to_date "$TO_DATE"

    # Pause between batches
    sleep 10
done
```

### 2. Handling Special Characters in Passwords

If your password contains special characters:

```bash
# Use single quotes to prevent shell interpretation
python main.py \
  --email user@example.com \
  --password 'P@ssw0rd!#$%' \
  --from_date 01/01/2024 \
  --to_date 31/01/2024
```

### 3. Running in Background

On Linux/Mac:

```bash
# Run in background and save output to log
nohup python main.py \
  --email user@example.com \
  --password mypass \
  --from_date 01/01/2024 \
  --to_date 31/12/2024 \
  > scraper.log 2>&1 &

# Check progress
tail -f scraper.log
```

### 4. Organizing Output by Date Range

```bash
#!/bin/bash

# Create dated output directory
DATE_RANGE="2024-Q1"
OUTPUT_DIR="output_$DATE_RANGE"
mkdir -p "$OUTPUT_DIR"

# Run scraper
python main.py \
  --email user@example.com \
  --password mypass \
  --from_date 01/01/2024 \
  --to_date 31/03/2024

# Move output files to dated directory
mv output/* "$OUTPUT_DIR/"
echo "Files saved to $OUTPUT_DIR/"
```

### 5. Consolidating Multiple Excel Files

After extraction, you might want to combine files:

```python
# consolidate.py
import pandas as pd
import glob

# Read all Excel files
excel_files = glob.glob('output/*.xlsx')
dfs = []

for file in excel_files:
    df = pd.read_excel(file)
    df['Source_File'] = file  # Track source
    dfs.append(df)

# Combine all dataframes
combined = pd.concat(dfs, ignore_index=True)

# Save consolidated file
combined.to_excel('consolidated_report.xlsx', index=False)
print(f"Consolidated {len(excel_files)} files into consolidated_report.xlsx")
```

## Troubleshooting Examples

### Issue: "Login Failed"

```bash
# Check if credentials are correct
echo "Testing credentials..."
python main.py \
  --email "correct-email@example.com" \
  --password "correct-password" \
  --from_date 01/01/2024 \
  --to_date 01/01/2024
```

### Issue: "No Data Found"

```bash
# Try a broader date range
python main.py \
  --email user@example.com \
  --password mypass \
  --from_date 01/01/2024 \
  --to_date 31/12/2024
```

### Issue: "TimeoutError"

```bash
# Process smaller date ranges
python main.py \
  --email user@example.com \
  --password mypass \
  --from_date 01/01/2024 \
  --to_date 07/01/2024  # Just one week
```

## Automation Examples

### Cron Job (Linux/Mac)

Run scraper daily at 2 AM:

```bash
# Edit crontab
crontab -e

# Add this line
0 2 * * * cd /path/to/dgw-scrapper && /path/to/dgw-scrapper/venv/bin/python main.py --email "$EMAIL" --password "$PASSWORD" --from_date $(date -d "yesterday" +\%d/\%m/\%Y) --to_date $(date -d "yesterday" +\%d/\%m/\%Y) >> /path/to/scraper.log 2>&1
```

### Windows Task Scheduler

Create a scheduled task to run weekly:

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Weekly
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `main.py --email user@example.com --password pass --from_date 01/01/2024 --to_date 31/01/2024`
7. Start in: `C:\path\to\dgw-scrapper`

---

For more examples and support, visit the [GitHub repository](https://github.com/alifnuryana/dgw-scrapper).
