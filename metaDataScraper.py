import os
import requests
import csv

# Get data from the API
url = 'https://web-cdn.api.bbci.co.uk/xd/content-collection/092c7c94-aa9b-4933-9349-eb942b3bde77?country=np&page=0&size=100'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    print('Failed to fetch data')

# Function to find the next file number
def get_next_file_name(base_name='todayData', extension='.csv'):
    i = 1
    while os.path.exists(f'{base_name}{i}{extension}'):
        i += 1
    return f'{base_name}{i}{extension}'

# Get the next available filename
file_name = get_next_file_name()

# Create the CSV file and write the data
with open(file_name, 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Date', 'Title', 'Path'])
    for article in data['data']:
        Path = article.get('path')
        Title = article.get('title')
        Date = article.get('firstPublishedAt')
        csv_writer.writerow([Date, Title, Path])

print(f'Data saved in {file_name}')
