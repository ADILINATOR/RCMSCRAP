import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv

def check_pdf_links(url):
    pdf_details = []

    # Fetch the webpage content
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return pdf_details

    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags with href attributes
    for link in soup.find_all('a', href=True):
        href = link['href']

        # Check if the link ends with .pdf
        if href.lower().endswith('.pdf'):
            # If the link is relative, make it absolute
            if not urlparse(href).netloc:
                href = urljoin(url, href)

            # Check if the PDF file is empty
            try:
                pdf_response = requests.head(href)
                pdf_response.raise_for_status()
                content_length = int(pdf_response.headers.get('Content-Length', 0))
                is_empty = content_length == 0
            except requests.exceptions.RequestException as e:
                print(f"Error checking {href}: {e}")
                is_empty = True  # Assume empty if there's an error checking the PDF

            # Collect PDF details
            pdf_details.append({'URL': href, 'IsEmpty': is_empty})

    return pdf_details

# Example usage:
if __name__ == "__main__":
    pdf_details = []

    # Using range() function to iterate 525 times
    for i in range(525):
        url = f"http://www.rcmbase.kz/en/karzav/karzav_card/{i + 1}/"
        pdf_details.extend(check_pdf_links(url))

    # Print or further process pdf_details as needed
    for detail in pdf_details:
        print(f"URL: {detail['URL']}, IsEmpty: {detail['IsEmpty']}")
