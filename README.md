# 🚀 DGW Scrapper

A powerful and automated web scraper for extracting LPJ data from the DGW Spartan platform. This tool streamlines the process of downloading and processing activity reports into organized Excel spreadsheets.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ✨ Features

- 🤖 **Automated Login**: Seamlessly authenticate with DGW Spartan platform
- 📅 **Date Range Filtering**: Extract data for specific time periods
- 📊 **Excel Export**: Generate clean, organized Excel reports
- 🎨 **Rich CLI Output**: Beautiful terminal interface with progress tracking
- ⚡ **Fast Processing**: Efficient Playwright-based browser automation
- 🔄 **Batch Processing**: Handle multiple LPJ documents in one run
- 📁 **Organized Output**: Automatically structured file naming and storage

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Output Format](#output-format)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- Valid DGW Spartan account credentials

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/alifnuryana/dgw-scrapper.git
cd dgw-scrapper
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers**

```bash
playwright install chromium
```

## 🚀 Usage

### Basic Command

```bash
python main.py --email YOUR_EMAIL --password YOUR_PASSWORD --from_date DD/MM/YYYY --to_date DD/MM/YYYY
```

### Example

```bash
python main.py --email user@example.com --password mypassword123 --from_date 01/01/2024 --to_date 31/01/2024
```

### Parameters

| Parameter     | Required | Description                    | Format     |
| ------------- | -------- | ------------------------------ | ---------- |
| `--email`     | ✅ Yes   | Your DGW Spartan email         | string     |
| `--password`  | ✅ Yes   | Your DGW Spartan password      | string     |
| `--from_date` | ✅ Yes   | Start date for data extraction | DD/MM/YYYY |
| `--to_date`   | ✅ Yes   | End date for data extraction   | DD/MM/YYYY |

## ⚙️ Configuration

The scraper is configured to:

- Navigate to the "Sudah Diproses" (Processed) tab
- Filter by document type: **LPJ**
- Extract the following data:
  - Activity Name
  - PO Name
  - Total Amount
  - Activity Count

### Output Directory

All generated files are saved in the `output/` directory, which is automatically created if it doesn't exist. The directory is cleaned before each run to ensure fresh data.

## 📄 Output Format

### File Naming Convention

Files are named using the following pattern:

```
{YYYY - Month} - {Submitted By} - {Activity Type 1} - {Activity Type 2} - {Proposal Name}.xlsx
```

**Example:**

```
2024 - January - John Doe - Workshop - Training - Employee Development.xlsx
```

### Excel Structure

The generated Excel files contain the following columns:

| Column        | Description              |
| ------------- | ------------------------ |
| Activity Name | Name of the activity     |
| PO Name       | Purchase Order name      |
| Total         | Total amount (in Rupiah) |
| Count         | Number of activities     |

Data is automatically:

- ✅ Cleaned and formatted
- ✅ Grouped by Activity Name and PO Name
- ✅ Aggregated with sum and count calculations
- ✅ Converted to proper numeric formats

## 🛠️ Troubleshooting

### Common Issues

<details>
<summary><strong>Browser fails to launch</strong></summary>

Ensure Playwright browsers are installed:

```bash
playwright install chromium
```

</details>

<details>
<summary><strong>Login fails</strong></summary>

- Verify your email and password are correct
- Check if your account has access to the Spartan platform
- Ensure you're not using special characters that need escaping
</details>

<details>
<summary><strong>TimeoutError during scraping</strong></summary>

This can occur if:

- Network connection is slow
- The page takes longer to load
- An item has no data table

The scraper will skip problematic items and continue processing others.

</details>

<details>
<summary><strong>Empty output folder</strong></summary>

- Check if the date range contains any LPJ documents
- Verify the filter settings match available documents
- Review the console output for any error messages
</details>

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Playwright](https://playwright.dev/) for reliable browser automation
- Uses [pandas](https://pandas.pydata.org/) for efficient data processing
- Enhanced with [Rich](https://rich.readthedocs.io/) for beautiful terminal output

## 📧 Contact

Alif Nuryana - [@alifnuryana](https://github.com/alifnuryana)

Project Link: [https://github.com/alifnuryana/dgw-scrapper](https://github.com/alifnuryana/dgw-scrapper)

---

<div align="center">
Made with ❤️ by <a href="https://github.com/alifnuryana">Alif Nuryana</a>
</div>
