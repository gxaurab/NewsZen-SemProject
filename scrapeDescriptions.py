import os
import requests
import csv
from bs4 import BeautifulSoup

base_url = 'https://bbc.com'

# generates the new file by checking , if the file already exists and if it does, it increments the file number by 1
def get_next_file_name(base_name='scraped_articles', extension='.csv'):
    i = 1
    while os.path.exists(f'{base_name}{i:02d}{extension}'): 
        i += 1
    return f'{base_name}{i:02d}{extension}'

# Get the next available filename
file_name = get_next_file_name()

# Create a new CSV file for storing the article details
with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Define headers for the CSV file
    csv_writer.writerow(['Headline', 'Description'])

    # Open the CSV that has the list of article paths
    with open('todayData1.csv', 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            req_path = row[2]  # Get the path (URL)
            full_url = base_url + req_path  # Construct full URL

            response = requests.get(full_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find the article tag
                article_tag = soup.find('article')
                
                if article_tag:
                    # Find the description divs with 'data-component' attribute
                    description_divs = article_tag.find_all('div', {'data-component': ['text-block', 'subheadline-block']})
                    
                    # Extract headline (assuming it's the title of the article)
                    headline = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'No headline found'
                    
                    # Extract descriptions
                    article_description = ''
                    for div in description_divs:
                        article_description += div.get_text(strip=True) + '\n'
                    
                    # Write the headline and description to the CSV file
                    csv_writer.writerow([headline, article_description.strip()])  # Strip to remove extra newline

print(f'Data saved in {file_name}')
