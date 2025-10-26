# Frequently Asked Questions (FAQ)

## General Questions

### What is DGW Scrapper?

DGW Scrapper is an automated web scraping tool designed to extract LPJ data from the DGW Spartan platform and convert it into organized Excel spreadsheets.

### Who should use this tool?

This tool is ideal for:

- Finance teams processing expense reports
- Administrators managing LPJ documents
- Data analysts needing structured data from Spartan
- Anyone who regularly downloads LPJ data from DGW Spartan

### Is this tool officially supported by DGW?

No, this is an independent, community-developed tool. It's not officially affiliated with or endorsed by DGW.

## Installation & Setup

### What are the system requirements?

- Python 3.8 or higher
- 2GB RAM minimum (4GB recommended)
- 500MB free disk space
- Internet connection
- Valid DGW Spartan account

### How do I install Python?

**Windows:**

1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer and check "Add Python to PATH"
3. Verify: Open CMD and type `python --version`

**Mac:**

```bash
brew install python3
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### The installation fails. What should I do?

1. Ensure Python 3.8+ is installed: `python3 --version`
2. Update pip: `pip install --upgrade pip`
3. Try installing dependencies one by one:
   ```bash
   pip install playwright
   pip install pandas
   pip install rich
   pip install openpyxl
   playwright install chromium
   ```

## Usage Questions

### How do I find my DGW Spartan credentials?

Your credentials are the same email and password you use to log in to [https://spartan.dgw.co.id/](https://spartan.dgw.co.id/).

### What date format should I use?

Always use `DD/MM/YYYY` format:

- ✅ Correct: `01/01/2024`
- ❌ Wrong: `2024-01-01`, `01-01-2024`, `1/1/2024`

### Can I extract data for multiple months at once?

Yes, but it's recommended to process month by month for better reliability:

```bash
# Works but not recommended for more than 3 months
python main.py --email user@example.com --password pass --from_date 01/01/2024 --to_date 31/03/2024

# Recommended: Process month by month
python main.py --email user@example.com --password pass --from_date 01/01/2024 --to_date 31/01/2024
python main.py --email user@example.com --password pass --from_date 01/02/2024 --to_date 29/02/2024
```

### Where are the output files saved?

All Excel files are saved in the `output/` directory in the project folder.

### What if no files are generated?

Possible reasons:

1. **No LPJ documents in date range**: Try a different date range
2. **Wrong credentials**: Verify your email and password
3. **Network issues**: Check your internet connection
4. **Filter mismatch**: The tool only processes LPJ documents

### Can I run this on a server without a display?

Yes! Playwright runs in headless mode by default, which works on servers without a GUI.

## Troubleshooting

### "Login failed" error

**Causes:**

- Incorrect email or password
- Special characters in password not properly escaped
- Account locked or expired

**Solutions:**

1. Verify credentials by logging in manually to Spartan
2. If password has special characters, wrap it in quotes:
   ```bash
   python main.py --email user@example.com --password 'P@ssw0rd!' --from_date 01/01/2024 --to_date 31/01/2024
   ```
3. Check if your account needs password reset

### "TimeoutError" during scraping

**Causes:**

- Slow internet connection
- Spartan platform is slow
- Page is taking too long to load

**Solutions:**

1. Try again with a smaller date range
2. Check your internet connection
3. The scraper will skip problematic items and continue with others

### "Module not found" error

**Cause:** Dependencies not installed properly

**Solution:**

```bash
# Reinstall all dependencies
pip install -r requirements.txt
playwright install chromium
```

### "Permission denied" when creating output directory

**Cause:** Insufficient permissions

**Solution:**

```bash
# Linux/Mac: Give yourself permissions
chmod -R 755 .

# Windows: Run as administrator or choose a different directory
```

### Browser won't launch

**Cause:** Playwright browsers not installed

**Solution:**

```bash
playwright install chromium
```

### Output files are empty or corrupted

**Causes:**

- Extraction failed silently
- Table structure changed on Spartan
- Data format issues

**Solutions:**

1. Check the console output for warnings
2. Try re-running for a specific date
3. Open an issue on GitHub with details

## Data & Security

### Is my password stored anywhere?

No. Credentials are only used during the session and are not stored. However, passing credentials via command-line arguments is visible in process lists. For better security, consider using environment variables.

### Is the extracted data secure?

The Excel files are saved locally on your computer without encryption. Protect them according to your organization's data security policies.

### Can others see my password in command history?

Yes, if you type it directly in the command line. To avoid this:

**Bash:**

```bash
# Add a space before the command to prevent it from being saved in history
 python main.py --email user@example.com --password mypass --from_date 01/01/2024 --to_date 31/01/2024
```

**Better approach - use environment variables:**

```bash
export DGW_EMAIL="user@example.com"
export DGW_PASSWORD="mypassword"
python main.py --email "$DGW_EMAIL" --password "$DGW_PASSWORD" --from_date 01/01/2024 --to_date 31/01/2024
```

## Performance

### How long does it take to process data?

Typical processing times:

- 1 day: ~30 seconds
- 1 week: ~2-3 minutes
- 1 month: ~5-10 minutes
- 1 year: ~1-2 hours (if run in one batch)

Actual time depends on:

- Number of LPJ documents
- Internet speed
- Computer performance

### Can I speed up the process?

Currently, no. The tool processes items sequentially to maintain reliability. Future versions may support parallel processing.

### Why does the output folder get cleaned each time?

This ensures you always have fresh data without duplicates. If you need to keep old data, move or rename the `output` folder before running the scraper.

## Advanced Usage

### Can I automate this to run daily?

Yes! See the [EXAMPLES.md](docs/EXAMPLES.md) file for cron job and Task Scheduler examples.

### Can I extract document types other than LPJ?

Not currently. The tool is specifically designed for LPJ documents. Support for other document types may be added in future versions.

### Can I customize the output format?

Not directly through command-line options. You would need to modify the `main.py` file. See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

### Can I run multiple instances simultaneously?

Not recommended. Multiple instances may interfere with each other. Instead, process different date ranges sequentially.

## Contributing & Support

### How can I report a bug?

1. Check if the issue already exists in [GitHub Issues](https://github.com/alifnuryana/dgw-scrapper/issues)
2. If not, create a new issue using the bug report template
3. Include:
   - Error messages
   - Steps to reproduce
   - Your environment (OS, Python version)

### How can I request a feature?

1. Check if the feature is already requested in [GitHub Issues](https://github.com/alifnuryana/dgw-scrapper/issues)
2. If not, create a new issue using the feature request template
3. Describe the feature and its use case

### Can I contribute code?

Absolutely! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. All contributions are welcome!

### Where can I get help?

1. Read this FAQ
2. Check the [README.md](README.md)
3. Review [EXAMPLES.md](docs/EXAMPLES.md)
4. Search [GitHub Issues](https://github.com/alifnuryana/dgw-scrapper/issues)
5. Create a new issue if you can't find an answer

## Legal & Compliance

### Is it legal to use this tool?

This tool automates actions that you can perform manually on the DGW Spartan platform. However:

- Ensure you have authorization to access the data
- Comply with your organization's IT policies
- Follow DGW's terms of service
- Don't use it to violate any laws or regulations

### Can I use this for commercial purposes?

Yes, the tool is licensed under the MIT License, which allows commercial use. However, respect the terms of service of the DGW Spartan platform.

### What's the license?

MIT License. See [LICENSE](LICENSE) file for details.

---

## Still have questions?

Can't find your answer here? Please [open an issue](https://github.com/alifnuryana/dgw-scrapper/issues/new) on GitHub, and we'll be happy to help!
