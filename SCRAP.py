from download import download_file_from_iframe, find_file_from_iframe, download_pdf_from_webpage, add_text_to_pdf
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import csv
import PyPDF2

# Function to download a PDF file (placeholder function)


def main():
    # url = "http://www.rcmbase.kz/en/karzav/karzav_card/{n}/"
    #
    # # Send a GET request to the URL
    # response = requests.get(url)
    #
    # # Check if request was successful
    # if response.status_code == 200:
    #     # Parse the HTML content
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #
    #     # Find all links (a tags) in the page
    #     links = soup.find_all('a', href=True)
    #     # Iterate through each link
    #     for link in links:
    #         href = link['href']
    #         i = 0
    #         # Assuming we're interested in PDF links, you can add more specific checks if needed
    #         if href.endswith('.pdf'):
    #             # Simulate downloading the PDF file
    #             print(href)
    #             if href.startswith('/'):
    #                 href = "http://www.rcmbase.kz" + href
    #             download_file_from_iframe(href, "/home/adl/kazdornii/karzav/dnld" + str(i))
    #             add_text_to_pdf("/home/adl/kazdornii/karzav/dnld" + str(i), href)
    #             i = i + 1
    #         else:
    #             print(f"Ignoring non-PDF link: {href}")
    # else:
    #     print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")



    base_url = "http://www.rcmbase.kz/en/karzav/karzav_card/{}"
    start_n = 1
    end_n = 545  # Set the range as needed
    i = 0
    links404 = [];
    # for n in range(start_n, end_n + 1):
    #     url = base_url.format(n)
    #     print(f"Processing URL: {url}")
    #
    #     # Send a GET request to the URL
    #     response = requests.get(url)
    #
    #     # Check if request was successful
    #     if response.status_code == 200:
    #         # Parse the HTML content
    #         soup = BeautifulSoup(response.content, 'html.parser')
    #
    #         # Find all links (a tags) in the page
    #         links = soup.find_all('a', href=True)
    #
    #         # Iterate through each link
    #
    #         for link in links:
    #             href = link['href']
    #
    #             # Assuming we're interested in PDF links, you can add more specific checks if needed
    #             if href.endswith('.pdf'):
    #                 # Simulate downloading the PDF file
    #                 print(f"Found PDF link: {href}")
    #                 if href.startswith('/'):
    #                     href = "http://www.rcmbase.kz" + href
    #                 download_path = f"/home/adl/kazdornii/karzav/dnld{i}.pdf"
    #                 links404 = download_file_from_iframe(href, download_path)
    #                 add_text_to_pdf(download_path, href)
    #                 i += 1
    #             else:
    #                 print(f"Ignoring non-PDF link: {href}")
    #     else:
    #         print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
    #
    # print(links404)


    def get_last_page_content(file_path):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if len(reader.pages) > 0:
                    last_page = reader.pages[-1]
                    text = last_page.extract_text().strip()
                    print(f"Extracted text from {file_path}")
                    return text
                else:
                    print(f"No pages found in {file_path}")
                    return ""
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""

    def find_files_and_save_to_csv(directory, csv_file):
        with open(csv_file, 'w', newline='') as csvfile:
            fieldnames = ['file_name', 'last_page_content']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        file_path = os.path.join(root, file)
                        file_size = os.path.getsize(file_path)
                        print(f"Checking file: {file_path}, Size: {file_size} bytes")
                        if file_size < 25000:  # Size in bytes
                            last_page_content = get_last_page_content(file_path)
                            writer.writerow({'file_name': file, 'last_page_content': last_page_content})

    if __name__ == "__main__":
        directory = '/home/adl/kazdornii/karzav/'  # Ensure this is the correct path
        csv_file = 'output.csv'
        find_files_and_save_to_csv(directory, csv_file)
        print(f"CSV file {csv_file} created successfully.")


if __name__ == "__main__":
    main()


