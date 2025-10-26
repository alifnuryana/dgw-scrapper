"""
DGW Scrapper - Automated LPJ Data Extraction Tool

This module provides automated web scraping functionality for the DGW Spartan platform.
It extracts LPJ documents within a specified date range
and generates organized Excel reports.

Author: Alif Nuryana
Repository: https://github.com/alifnuryana/dgw-scrapper
License: MIT
"""

import argparse
import glob
import os
import string
from datetime import datetime
import pandas as pd
from playwright.sync_api import sync_playwright, expect, TimeoutError
from io import StringIO
import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.progress import track


def main():
    """
    Main execution function for the DGW scraper.
    
    This function orchestrates the entire scraping process:
    1. Parses command-line arguments
    2. Authenticates with DGW Spartan
    3. Navigates to the inbox and applies filters
    4. Extracts LPJ documents
    5. Processes and exports data to Excel files
    
    The function uses Playwright for browser automation and pandas for data processing.
    All output files are saved in the 'output/' directory with descriptive filenames.
    """
    # Configure rich logging for beautiful terminal output
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()]
    )
    logger = logging.getLogger("dgw-scrapper")
    console = Console()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='DGW Scrapper - Extract LPJ data from DGW Spartan platform',
        epilog='Example: python main.py --email user@example.com --password pass123 --from_date 01/01/2024 --to_date 31/01/2024'
    )
    parser.add_argument('--email', required=True, help='DGW Spartan account email')
    parser.add_argument('--password', required=True, help='DGW Spartan account password')
    parser.add_argument('--from_date', required=True, help='Start date for data extraction (DD/MM/YYYY)')
    parser.add_argument('--to_date', required=True, help='End date for data extraction (DD/MM/YYYY)')

    args = parser.parse_args()

    # Sanitize credentials by removing whitespace and punctuation
    email = args.email.strip(string.whitespace + string.punctuation)
    password = args.password.strip(string.whitespace + string.punctuation)

    logger.info("Launching browser and logging in...")
    with sync_playwright() as playwright:
        # Initialize Chromium browser in headless mode
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        # Navigate to DGW Spartan and perform login
        page.goto('https://spartan.dgw.co.id/')
        page.wait_for_url('https://spartan.dgw.co.id/login/')

        page.get_by_role('textbox', name='Email').fill(email)
        page.get_by_role('textbox', name='Password').fill(password)
        page.get_by_role('button', name='Login').click()
        page.wait_for_url('https://spartan.dgw.co.id/')

        logger.info("Navigating to Inbox...")
        page.get_by_role('button', name='Inbox').click()
        page.wait_for_url('https://spartan.dgw.co.id/inbox/')

        # Navigate to "Sudah Diproses" (Processed) tab and open filters
        page.get_by_role('tab', name='Sudah Diproses').click()
        page.get_by_role('button', name='Filter').click()

        # Set the "from" date using the date picker
        page.get_by_role('button', name='Choose date').first.click()
        from_date = datetime.strptime(args.from_date, '%d/%m/%Y')
        # Navigate to the correct month/year for "from" date
        while True:
            current_calendar = page.locator(".MuiPickersCalendarHeader-label").first.inner_text().strip()
            current_datetime = datetime.strptime(current_calendar, "%B %Y")

            if (current_datetime.year, current_datetime.month) < (from_date.year, from_date.month):
                page.get_by_role("button", name="Next month").first.click()
            elif (current_datetime.year, current_datetime.month) > (from_date.year, from_date.month):
                page.get_by_role("button", name="Previous month").first.click()
            else:
                page.get_by_role('gridcell', name=str(from_date.day)).first.click()
                break

        # Set the "to" date using the date picker
        page.get_by_role('button', name='Choose date').last.click()
        to_date = datetime.strptime(args.to_date, '%d/%m/%Y')
        # Navigate to the correct month/year for "to" date
        while True:
            current_calendar = page.locator(".MuiPickersCalendarHeader-label").last.inner_text().strip()
            current_datetime = datetime.strptime(current_calendar, "%B %Y")

            if (current_datetime.year, current_datetime.month) < (to_date.year, to_date.month):
                page.get_by_role("button", name="Next month").last.click()
            elif (current_datetime.year, current_datetime.month) > (to_date.year, to_date.month):
                page.get_by_role("button", name="Previous month").last.click()
            else:
                page.get_by_role('gridcell', name=str(to_date.day)).last.click()
                break

        # Filter by document type: LPJ
        page.get_by_role("button", name="Document", exact=True).click()
        page.get_by_role("option", name="LPJ").click()
        page.get_by_role("button", name="Search").click()

        # Wait for search results to load completely
        page.wait_for_load_state('networkidle')
        page.locator(".MuiCircularProgress-root").wait_for(state="detached")

        # Get the list of all LPJ items
        ul = page.locator('xpath=/html/body/div/div[2]/main/div[2]/div[1]/div[5]/div/div/ul')

        # Prepare output directory
        folder_path = 'output'
        os.makedirs(folder_path, exist_ok=True)

        # Clean previous output files
        logger.info("Cleaning output folder...")
        for file_path in glob.glob(os.path.join(folder_path, '*')):
            os.remove(file_path)

        items = ul.locator('li').all()
        logger.info(f"Found {len(items)} items to process.")
        
        # Process each LPJ document
        for index, item in enumerate(track(items, description="Processing items...")):
            # Extract document code and click to open details
            code = item.locator("xpath=/div/div/div[2]/div[1]/p[2]").inner_html()
            item.click()
            expect(page.get_by_role("heading", name=code)).to_be_visible()

            # Extract metadata for filename generation
            submitted_by = page.get_by_role("textbox", name="Submitted By (Dikirim Oleh)").input_value()
            activity_type_first = page.get_by_role("textbox", name="Activity Type (Tipe Aktivitas)").first.input_value()
            activity_type_second = page.get_by_role("textbox", name="Activity Type (Tipe Aktivitas)").nth(1).input_value()
            proposal_name = page.get_by_role("textbox", name="Proposal Name").input_value()
            lpj_date = page.get_by_role("textbox", name="LPJ Date").input_value()
            lpj_date = datetime.strftime(datetime.strptime(lpj_date, "%d/%m/%Y"), '%Y - %B')

            # Create descriptive filename
            filename = f"{lpj_date} - {submitted_by} - {activity_type_first} - {activity_type_second} - {proposal_name}"

            try:
                # Locate and extract the activity table HTML
                table_locator = page.get_by_role("table", name="activity table").last
                table_html = table_locator.evaluate("el => el.outerHTML")

                # Parse HTML table into pandas DataFrame
                df = pd.read_html(StringIO(table_html))[0]

                # Remove unnecessary columns
                df = df.drop(columns=[
                    'Activity Date', 'Provinsi', 'Kabupaten / Kota', 'Description',
                    'Total Activities', 'UOM', 'Amount/Activity', 'Sub Total Activity',
                    'Gifts', 'Total Gifts Item', 'Gift Amount', 'Action'
                ])
                
                # Clean text fields
                df['Activity Name'] = df['Activity Name'].str.replace("Select", "", case=False, regex=True)
                df['PO Name'] = df['PO Name'].str.replace("Select", "", case=False, regex=True)
                
                # Clean and convert Total column to numeric (Rupiah to integer)
                df['Total'] = (
                    df['Total']
                    .astype(str)
                    .str.replace(r'\xa0', '', regex=True)  # Remove non-breaking spaces
                    .str.replace(r'Rp', '', regex=True)     # Remove currency symbol
                    .str.replace(r'\.', '', regex=True)     # Remove thousand separators
                    .str.strip()
                    .astype('int64')
                )
                
                # Aggregate data by Activity Name and PO Name
                df = (
                    df.groupby(["Activity Name", "PO Name"], as_index=False)
                    .agg(
                        Total=("Total", "sum"),      # Sum of all amounts
                        Count=("Total", "size")      # Count of activities
                    )
                )

                # Export to Excel
                output_path = os.path.join(folder_path, f"{filename}.xlsx")
                df.to_excel(output_path, index=False)
                logger.info(f"Saved: {output_path}")
            except TimeoutError:
                # Skip items that timeout and continue with the next one
                logger.warning(f"TimeoutError for item {index+1}: {filename}")
                continue


if __name__ == '__main__':
    """Entry point for the script when run from command line."""
    main()
