import requests
from bs4 import BeautifulSoup
from github import Github
import time

# GitHub credentials
github_token = 'your_github_token'
repo_name = 'your_repo_name'
file_path = 'path/to/recorded_data.txt'

# Target URL
url = 'https://example.com'

# Function to scrape the webpage
def scrape_page():
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract relevant data from the webpage
        data = soup.find('div', class_='example-class').text  # Adjust based on the actual HTML structure

        return data
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return None

# Function to update GitHub repository with changes
def update_github(data):
    g = Github(github_token)
    repo = g.get_repo(repo_name)

    # Get the content of the existing file
    try:
        contents = repo.get_contents(file_path)
        existing_data = contents.decoded_content.decode()
    except Exception as e:
        existing_data = ''

    # Check if there are changes
    if data != existing_data:
        # Update the file on GitHub
        repo.update_file(
            path=file_path,
            message='Update data',
            content=data,
            sha=contents.sha
        )
        print('Changes detected and recorded on GitHub.')
    else:
        print('No changes detected.')

# Main loop to run the scraper every 5 hours
while True:
    data = scrape_page()
    if data is not None:
        update_github(data)

    # Sleep for 5 hours
    time.sleep(5 * 60 * 60)