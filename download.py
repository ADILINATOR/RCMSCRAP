import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

import re

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os


def download_file_from_iframe(page_url, output_path):
    links404 = []

    try:
        # Get the HTML content of the page
        response = requests.get(page_url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the iframe and get the src attribute
        iframe = soup.find('iframe')
        if iframe is None:
            print('No iframe found on the page.')
            return

        iframe_src = iframe['src'].split('(')[0]  # Remove any part after '('
        iframe_src = iframe_src.strip()  # Remove any leading/trailing whitespace

        # If the src is a relative URL, convert it to an absolute URL
        if not iframe_src.startswith('http'):
            iframe_src = urljoin(page_url, iframe_src)

        try:
            # Download the file from the iframe URL
            file_response = requests.get(iframe_src, stream=True)
            file_response.raise_for_status()

            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Save the file locally
            with open(output_path, 'wb') as file:
                for chunk in file_response.iter_content(chunk_size=8192):
                    if chunk:  # Filter out keep-alive new chunks
                        file.write(chunk)

            print(f'File downloaded successfully: {output_path}')

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f'Error 404: File not found at {iframe_src}')
                links404.append(iframe_src)
            else:
                raise

    except requests.exceptions.RequestException as e:
        print(f'Error occurred while fetching the page: {e}')

    return links404




# Example usage


def find_file_from_iframe(page_url, output_path):
    try:
        # Get the HTML content of the page
        response = requests.get(page_url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the iframe and get the src attribute
        iframe = soup.find('iframe')
        if iframe is None:
            print('No iframe found on the page.')
            return None

        iframe_src = iframe['src']

        # If the src is a relative URL, convert it to an absolute URL
        if not iframe_src.startswith('http'):
            iframe_src = urljoin(page_url, iframe_src)

        print(f'File found successfully: {output_path}')
        return iframe_src

    except requests.exceptions.RequestException as e:
        print(f'Error fetching page content: {e}')
        return None





def download_pdf_from_webpage(url, save_path):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the <iframe> tag that contains the PDF
        iframe = soup.find('iframe')

        # Extract the source URL of the PDF from the iframe's src attribute
        if iframe:
            pdf_url = iframe['src']

            # If the URL is relative, construct the full URL
            if pdf_url.startswith('/'):
                pdf_url = "http://www.rcmbase.kz" + pdf_url
            print(pdf_url)
            # Download the PDF file
            response = requests.get(pdf_url)
            if response.status_code == 200:
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"PDF downloaded successfully and saved to: {save_path}")
            else:
                print(f"Failed to download PDF from {pdf_url}. Status code: {response.status_code}")
        else:
            print("No <iframe> found on the webpage.")
    else:
        print(f"Failed to fetch webpage {url}. Status code: {response.status_code}")

# def add_text_to_pdf(pdf_path, text):
#     """Adds text to the end of a PDF document.
#
#     Args:
#         pdf_path: Path to the existing PDF file.
#         text: The text to be added.
#     """
#     with open(pdf_path, 'rb') as pdf_file:
#         reader = PdfReader(pdf_file)
#         writer = PdfWriter()
#
#         # Add all existing pages
#         for page_num in range(len(reader.pages)):
#             writer.add_page(reader.pages[page_num])
#
#         # Create a new PDF with ReportLab containing the text
#         packet = io.BytesIO()
#         can = canvas.Canvas(packet, pagesize=letter)
#         can.setFont("Helvetica", 10)
#         can.drawString(100, 50, text)
#         can.save()
#
#         # Move to the beginning of the StringIO buffer
#         packet.seek(0)
#         new_pdf = PdfReader(packet)
#         new_page = new_pdf.pages[0]
#
#         # Add the new page to the writer
#         writer.add_page(new_page)
#
#         # Write the modified PDF to a new file
#         with open(f"{pdf_path}", 'wb') as output_file:
#             writer.write(output_file)
def add_text_to_pdf(pdf_path, text):
    """Adds text to the end of a PDF document.

    Args:
        pdf_path: Path to the existing PDF file.
        text: The text to be added.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()

            # Add all existing pages
            for page_num in range(len(reader.pages)):
                writer.add_page(reader.pages[page_num])

            # Create a new PDF with ReportLab containing the text
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)

            # Define text properties
            text_box_width = 400  # width of the text box (you can adjust this)
            x, y = 50, 700  # Starting position (x, y) for the text box

            # Add text with desired formatting (adjust font and position as needed)
            can.setFont("Helvetica", 10)

            # Manually wrap text
            max_line_length = int(text_box_width / 6)  # Approximate character limit per line
            lines = []
            while len(text) > 0:
                if len(text) > max_line_length:
                    # Find the last space within the limit
                    wrap_at = text.rfind(' ', 0, max_line_length)
                    if wrap_at == -1:
                        wrap_at = max_line_length
                    lines.append(text[:wrap_at])
                    text = text[wrap_at:].lstrip()
                else:
                    lines.append(text)
                    break

            for line in lines:
                can.drawString(x, y, line)
                y -= 12  # Move down for the next line (adjust the space between lines as needed)

            can.save()

            # Move to the beginning of the StringIO buffer
            packet.seek(0)
            new_pdf = PdfReader(packet)
            new_page = new_pdf.pages[0]

            # Add the new page to the writer
            writer.add_page(new_page)

            # Write the modified PDF to a new file
            with open(pdf_path, 'wb') as output_file:
                writer.write(output_file)

        print(f'Text added successfully to {pdf_path}')

    except FileNotFoundError:
        print(f'File not found: {pdf_path}')
    except Exception as e:
        print(f'An error occurred: {e}')


