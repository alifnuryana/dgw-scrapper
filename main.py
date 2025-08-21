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
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()]
    )
    logger = logging.getLogger("dgw-scrapper")
    console = Console()

    parser = argparse.ArgumentParser()
    parser.add_argument('--email', required=True, help='Email')
    parser.add_argument('--password', required=True, help='Password')
    parser.add_argument('--from_date', required=True, help='From date (DD/MM/YYYY)')
    parser.add_argument('--to_date', required=True, help='To date (DD/MM/YYYY)')

    args = parser.parse_args()

    email = args.email.strip(string.whitespace + string.punctuation)
    password = args.password.strip(string.whitespace + string.punctuation)

    logger.info("Launching browser and logging in...")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto('https://spartan.dgw.co.id/')
        page.wait_for_url('https://spartan.dgw.co.id/login/')

        page.get_by_role('textbox', name='Email').fill(email)
        page.get_by_role('textbox', name='Password').fill(password)
        page.get_by_role('button', name='Login').click()
        page.wait_for_url('https://spartan.dgw.co.id/')

        logger.info("Navigating to Inbox...")
        page.get_by_role('button', name='Inbox').click()
        page.wait_for_url('https://spartan.dgw.co.id/inbox/')

        page.get_by_role('tab', name='Sudah Diproses').click()
        page.get_by_role('button', name='Filter').click()

        page.get_by_role('button', name='Choose date').first.click()
        from_date = datetime.strptime(args.from_date, '%d/%m/%Y')
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

        page.get_by_role('button', name='Choose date').last.click()
        to_date = datetime.strptime(args.to_date, '%d/%m/%Y')
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

        page.get_by_role("button", name="Document", exact=True).click()
        page.get_by_role("option", name="LPJ").click()
        page.get_by_role("button", name="Search").click()

        page.wait_for_load_state('networkidle')
        page.locator(".MuiCircularProgress-root").wait_for(state="detached")

        ul = page.locator('xpath=/html/body/div/div[2]/main/div[2]/div[1]/div[5]/div/div/ul')

        folder_path = 'output'
        os.makedirs(folder_path, exist_ok=True)

        logger.info("Cleaning output folder...")
        for file_path in glob.glob(os.path.join(folder_path, '*')):
            os.remove(file_path)

        items = ul.locator('li').all()
        logger.info(f"Found {len(items)} items to process.")
        for index, item in enumerate(track(items, description="Processing items...")):
            code = item.locator("xpath=/div/div/div[2]/div[1]/p[2]").inner_html()
            item.click()
            expect(page.get_by_role("heading", name=code)).to_be_visible()

            submitted_by = page.get_by_role("textbox", name="Submitted By (Dikirim Oleh)").input_value()
            activity_type_first = page.get_by_role("textbox", name="Activity Type (Tipe Aktivitas)").first.input_value()
            activity_type_second = page.get_by_role("textbox", name="Activity Type (Tipe Aktivitas)").nth(1).input_value()
            proposal_name = page.get_by_role("textbox", name="Proposal Name").input_value()
            lpj_date = page.get_by_role("textbox", name="LPJ Date").input_value()
            lpj_date = datetime.strftime(datetime.strptime(lpj_date, "%d/%m/%Y"), '%Y - %B')

            filename = f"{lpj_date} - {submitted_by} - {activity_type_first} - {activity_type_second} - {proposal_name}"

            try:
                table_locator = page.get_by_role("table", name="activity table").last
                table_html = table_locator.evaluate("el => el.outerHTML")

                df = pd.read_html(StringIO(table_html))[0]

                df = df.drop(columns=[
                    'Activity Date', 'Provinsi', 'Kabupaten / Kota', 'Description',
                    'Total Activities', 'UOM', 'Amount/Activity', 'Sub Total Activity',
                    'Gifts', 'Total Gifts Item', 'Gift Amount', 'Action'
                ])
                df['Activity Name'] = df['Activity Name'].str.replace("Select", "", case=False, regex=True)
                df['PO Name'] = df['PO Name'].str.replace("Select", "", case=False, regex=True)
                df['Total'] = (
                    df['Total']
                    .astype(str)
                    .str.replace(r'\xa0', '', regex=True)
                    .str.replace(r'Rp', '', regex=True)
                    .str.replace(r'\.', '', regex=True)
                    .str.strip()
                    .astype('int64')
                )
                df = (
                    df.groupby(["Activity Name", "PO Name"], as_index=False)
                    .agg(
                        Total=("Total", "sum"),
                        Count=("Total", "size")
                    )
                )

                output_path = os.path.join(folder_path, f"{filename}.xlsx")
                df.to_excel(output_path, index=False)
                logger.info(f"Saved: {output_path}")
            except TimeoutError:
                logger.warning(f"TimeoutError for item {index+1}: {filename}")
                continue



if __name__ == '__main__':
    main()