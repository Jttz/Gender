import csv
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time

token = 'your_github_access_token'

repoName = 'Enter project name'

headers = {
    'Content-Type': 'application/vnd.github.v3+json',
    'Authorization': f'token {token}'
}

page = 1
contributors = []

#Set up a session with a retry policy
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

while True:
    time.sleep(1)  # Adhere to the speed limit of GitHub API
    url = f'https://api.github.com/repos/{repoName}/contributors?per_page=100&page={page}'
    r = session.get(url, headers=headers)

    print('-------------------------------------')
    print('Current page number:', page)
    print('Project name:', repoName)
    print('HTTP response code:', r.status_code)

    if r.status_code == 200:
        jsonList = r.json()
        if not jsonList:
            break

        for contributor in jsonList:
            login = contributor.get('login', None)
            if login:
                print(f"Login: {login}")
                contributors.append({'login': login})

        page += 1
    else:
        print('Request error, wait for a while and try again..')
        time.sleep(10)

#Extract login field
logins = [contributor['login'] for contributor in contributors]

# Specify the save path for CSV files
file_name = os.path.join(os.path.expanduser("~"), f"{repoName.replace('/', '_')}_logins.csv")

# Store logins in a CSV file
with open(file_name, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['login'])
    writer.writerows([[login] for login in logins])

print(f"Logins have been stored in a file: {file_name}")
