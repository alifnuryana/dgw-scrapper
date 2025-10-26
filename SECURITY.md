# Security Policy

## Supported Versions

Currently, the following versions of DGW Scrapper are being supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of DGW Scrapper seriously. If you discover a security vulnerability, please follow these steps:

### How to Report

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. Email the maintainer directly at [your-email@example.com]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact
   - Suggested fix (if available)

### What to Expect

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Varies based on severity
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: 30-90 days

### Disclosure Policy

- We will acknowledge your report within 48 hours
- We will keep you informed about the progress
- We will credit you in the fix announcement (unless you prefer to remain anonymous)
- We will publicly disclose the vulnerability after a fix is released

## Security Best Practices

When using DGW Scrapper:

### Credential Management

- ⚠️ **NEVER** hardcode credentials in scripts
- ⚠️ **NEVER** commit credentials to version control
- ✅ Use environment variables for sensitive data
- ✅ Use password managers or secure vaults
- ✅ Rotate credentials regularly

### Example: Using Environment Variables

```bash
# Set environment variables
export DGW_EMAIL="your-email@example.com"
export DGW_PASSWORD="your-secure-password"

# Use in command
python main.py --email "$DGW_EMAIL" --password "$DGW_PASSWORD" --from_date 01/01/2024 --to_date 31/01/2024
```

### Data Protection

- 🔒 Ensure output files are stored securely
- 🔒 Be careful when sharing Excel files (they may contain sensitive data)
- 🔒 Use appropriate file permissions on output directory
- 🔒 Delete old output files that are no longer needed

### Network Security

- 🌐 Always verify you're connecting to the legitimate DGW Spartan domain
- 🌐 Use secure networks (avoid public Wi-Fi for sensitive operations)
- 🌐 Keep Playwright and dependencies updated

## Known Security Considerations

1. **Credential Handling**: This tool requires passing credentials via command-line arguments. Consider using a more secure credential management system for production use.

2. **Browser Automation**: The tool launches a browser instance. Ensure your system is secure and up-to-date.

3. **Data Storage**: Output files contain potentially sensitive business data. Protect them accordingly.

## Updates and Patches

- Security patches are released as soon as possible
- Update notifications will be posted in GitHub releases
- Subscribe to repository notifications to stay informed

## Acknowledgments

We appreciate security researchers who responsibly disclose vulnerabilities. Contributors will be acknowledged in our security advisories (with permission).

---

Last Updated: October 27, 2025
